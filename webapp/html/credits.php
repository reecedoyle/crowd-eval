<?php 
	error_reporting(E_ALL);
	ini_set('display_errors', 1);
	require_once('../inc/functions.php');
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
			if ($_SERVER["REQUEST_METHOD"] == "POST") {
				$topic = $_POST['topic'];
				$clicks = array( // point to current position in results for each ranker
					"DuckDuckGo" => $_POST['DuckDuckGo'],
					"UCL" => $_POST['UCL'],
					"Cloud" => $_POST['Cloud'],
					);
				$credits = array(
					"DuckDuckGo" => 0,
					"UCL" => 0,
					"Cloud" => 0,
					);
				// assign credit to each ranker proportional to number of rankers than which they got more clicks
				foreach ($clicks as $ranker1 => $click1) {
					foreach ($clicks as $ranker2 => $click2) {
						if ($click1 > $click2 && $ranker1 != $ranker2) {
							$credits[$ranker1] ++;
						}
					}
				}
				/* debug:
				foreach ($credits as $ranker => $credit) {
					echo '<script type="text/javascript">console.log("'.$ranker.': '.$credit.'");</script>';
				}
				*/
				foreach ($credits as $ranker => $credit) {
					if ($credit == 0) {
						continue;
					}
					try {
						$conn = new PDO("mysql:host=$db_host;dbname=$db_name;charset=utf8mb4", $db_user, $db_pass);
						$sql = 'INSERT INTO Feedback
										(source, topic, credit) VALUES (:ranker, :topic, :cred)
										ON DUPLICATE KEY
										UPDATE
										credit = (@cur_credit := credit) + :cred';
						$stmt = $conn->prepare($sql);
						$stmt->bindParam(':ranker', $ranker);
						$stmt->bindParam(':topic', $topic);
						$stmt->bindParam(':cred', $credit);
						$stmt->execute();
					}
					catch (PDOException $pe) {
						die("Could not connect to the database $db_name: " . $pe->getMessage());
					}
				}
				if(empty($_POST['continue'])){
					echo '<script>window.location.replace("/");</script>';
				}
				echo '<script>window.location.replace("eval.php");</script>';
			}
			else{
				echo '<script>window.location.replace("/");</script>';
			}
		?>
	</body>
</html>