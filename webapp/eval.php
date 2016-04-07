<?php 
	error_reporting(E_ALL);
	ini_set('display_errors', 1);
	require_once('functions.php');
	//echo "Session before update: ",print_r($_SESSION, true),"<br>--------<br>";
	updateSession();
	//echo "Session after update: ",print_r($_SESSION, true),"<br>--------<br>";
	//destroySession();
?>
<html>
	<head>
		<title>Crowd Eval</title>
		<link rel="stylesheet" type="text/css" href="css/reset.css">
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
		<link href='http://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,400,300,600,700' rel='stylesheet' type='text/css'>	
		<link href="css/eval.css" rel="stylesheet">
		<meta charset="utf-8">
	</head>
	<body>
		<?php
			//destroySession();
			//echo "Session in body: ",print_r($_SESSION, true),"<br>--------<br>";
			if (!isset($_SESSION['topics'])){
				try {
					$conn = new PDO("mysql:host=$db_host;dbname=$db_name;charset=utf8mb4", $db_user, $db_pass);
					$sql = 'SELECT * FROM Topics';
					$stmt = $conn->prepare($sql);
					$stmt->execute();
					$_SESSION['topics'] = $stmt->fetchAll(PDO::FETCH_ASSOC);
					echo "Retrieved from DB","<br>--------<br>";
				}
				catch (PDOException $pe) {
					die("Could not connect to the database $db_name: " . $pe->getMessage());
				}
			}
			$topics = &$_SESSION['topics'];
			if (empty($topics)) {
				echo '<script>window.location.replace("complete.php");</script>';
			}
			else {
				$rand_key = array_rand($topics, 1);
				/*
				echo print_r($topics, true),"<br>--------<br>";
				echo "Len: ",count($topics),"<br>--------<br>";
				echo "Key: ",print_r($rand_key, true),"<br>--------<br>";
				echo print_r($topics[$rand_key], true),"<br>--------<br>";
				echo "Len: ",count($topics),"<br>--------<br>";
				echo "Session after body: ",print_r($_SESSION, true),"<br>--------<br>";
				echo print_r($topic, true),"<br>--------<br>";
				echo print_r($topic_id, true),"<br>--------<br>";
				echo print_r($query, true),"<br>--------<br>";
				*/
				$topic = $topics[$rand_key]['topic'];
				$topic_id = $topics[$rand_key]['id'];
				$query = $topics[$rand_key]['query'];
				unset($topics[$rand_key]);

				echo '<script type="text/javascript">
								var clicks = { // TODO hardcode this to make it work
									"UCL" : 0,
									"DuckDuckGo" : 0,
								};
								function recordClick(ranker) {
									clicks[ranker] += 1;
									document.getElementById(ranker.concat(\'clicks\')).innerHTML = clicks[ranker];
								}
								function submitClicks() { // do this manually for now
									document.clickForm.UCL.value = clicks["UCL"];;
									document.clickForm.DuckDuckGo.value = clicks["DuckDuckGo"];
									document.forms["clickForm"].submit();
								}
							</script>';
				// now get results
				try {
					$conn = new PDO("mysql:host=$db_host;dbname=$db_name;charset=utf8mb4", $db_user, $db_pass);
					$sql = 'SELECT title, link, snippet
									FROM DuckResults
									WHERE topic = :topic_id
									ORDER BY rank ASC
									LIMIT 10';
					$stmt = $conn->prepare($sql);
					$stmt->bindParam(':topic_id', $topic_id);
					$stmt->execute();
					$duck_results = $stmt->fetchAll(PDO::FETCH_ASSOC);
					$sql = 'SELECT title, link, snippet
									FROM UCLResults
									WHERE topic = :topic_id
									ORDER BY rank ASC
									LIMIT 10';
					$stmt = $conn->prepare($sql);
					$stmt->bindParam(':topic_id', $topic_id);
					$stmt->execute();
					$ucl_results = $stmt->fetchAll(PDO::FETCH_ASSOC);
					// TODO: get custom results here too
				}
				catch (PDOException $pe) {
					die("Could not connect to the database $db_name: " . $pe->getMessage());
				}
				
				$results = array(
					"DuckDuckGo" => &$duck_results,
					"UCL" => &$ucl_results,
					);
				$rankers = array_keys($results);
				// balanced interleaving, so randomly choose the order of rankers:
				shuffle($rankers);
				$pointers = array( // point to current position in results for each ranker
					"DuckDuckGo" => 0,
					"UCL" => 0,
					);
				$interleaved = array(); // stores the final results
				$order = array();
				$no_more = false; // used to signal one ranker has run out of results
				$count = 0;
				while (true) {
					//echo "Round: ",print_r($count, true),"<br>--------<br>";
					foreach ($rankers as $key => $ranker) {
						$count++;
						//echo "Round: ",print_r($ranker, true),"<br>--------<br>";
						$add_result = true;
						do {
							if ($pointers[$ranker] >= count($results[$ranker])) { // check there are results left for this ranker
								$add_result = false;
								break;
							}
							else{
								$result = $results[$ranker][$pointers[$ranker]];
								$pointers[$ranker]++; //increment the pointer to the next result for that ranker
							}
						} while (array_key_exists($result['link'], $interleaved)); // link already submitted by another ranker
						if ($add_result) {
							$interleaved[$result['link']] = $result;
							$order[$count] = $ranker;
						}
						else{ // no result from this ranker so quit after this round
							$no_more = true;
						}
					}
					if ($no_more) {
						break;
					}
				}
				// display query
				echo '<div class="container">
								<div class="well">
									<h3>'.$topic.'</h3>
									<p>UCL Clicks: <a id="UCLclicks">0</a></p>
									<p>Duck Clicks: <a id="DuckDuckGoclicks">0</a></p>
									<form id="clickForm" name="clickForm" method="post" action="credits.php">';
				echo '<input type="hidden" name="topic" id="topic" value="'.$topic_id.'">';
				foreach ($rankers as $key => $ranker) {
					echo '<input type="hidden" name="'.$ranker.'" id="'.$ranker.'" value="">';
				}
				echo '<button class="btn btn-success btn-md" title="reply" onclick="submitClicks();">' .
									'<i class="fa fa-reply"></i> reply' .
							'</button>
							</form>
						</div>';

				// display results!
				$count = 0;
				echo '<div class="col-md-8 col-md-offset-2">';
				foreach ($interleaved as $key => $result) {
					$count++;
					echo '<div class="panel panel-default">
									<div class="panel-heading">
										<h3 class="panel-title">
											<a href="'.htmlspecialchars($result['link']).'" target="_blank" style="target-new: tab;" onclick="recordClick(\''.$order[$count].'\');">'.htmlspecialchars($result['title']).'</a>
										</h3>
									</div>
									<div class="panel-body">
										'.htmlspecialchars($result['snippet']).'...
									</div>
								</div>';
					// now the modal
								/*
								<button class="btn btn-primary view-page" data-toggle="modal" data-target="#'.$count.'modal">
												View
											</button>
					echo '<div id="'.$count.'modal" class="modal fade modal-lg" tabindex="-1" role="dialog" aria-labelledby="iframe modal">
									<div class="modal-dialog modal-lg">
										<div class="modal-content">
											<iframe src="'.$result['link'].'" style="zoom:0.8" width="99.6%" height="250" frameborder="0"></iframe>
										</div>
									</div>
								</div>';*/
				}
				echo '</div>';
			}







			?>
		</div>
		<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
		<!-- Include all compiled plugins (below), or include individual files as needed -->
		<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>
	</body>
</html>