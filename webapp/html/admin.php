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
		<div class="container">
			<br>
			<div class="panel panel-default">
				<div class="panel-heading">
					Feedback
				</div>
				<div class="panel-body">
					<table class="table">
						<thead>
							<tr>
								<th>Topic</th>
								<th>Ranker</th>
								<th>Credit</th>
							</tr>
						</thead>
						<tbody>
							<?php
								// now get results
								try {
									$conn = new PDO("mysql:host=$db_host;dbname=$db_name;charset=utf8mb4", $db_user, $db_pass);
									$sql = 'SELECT source, topic, credit
													FROM Feedback
													ORDER BY topic, source';
									$stmt = $conn->prepare($sql);
									$stmt->execute();
									$feedback = $stmt->fetchAll(PDO::FETCH_ASSOC);
								}
								catch (PDOException $pe) {
									die("Could not connect to the database $db_name: " . $pe->getMessage());
								}

								foreach ($feedback as $row) {
									echo('<tr>');
									echo('<td>' . $row['topic'] . '</td>');
									echo('<td>' . $row['source'] . '</td>');
									echo('<td>' . $row['credit'] . '</td>');
									echo('</tr>');
								}
							?>
						</tbody>
					</table>
				</div>
			</div>
			<br>
			<div class="panel panel-default">
				<div class="panel-heading">
					LastFeedback
				</div>
				<div class="panel-body">
					<table class="table">
						<thead>
							<tr>
								<th>Topic</th>
								<th>Ranker</th>
								<th>Credit</th>
							</tr>
						</thead>
						<tbody>
							<?php
								// now get results
								try {
									$conn = new PDO("mysql:host=$db_host;dbname=$db_name;charset=utf8mb4", $db_user, $db_pass);
									$sql = 'SELECT source, topic, credit
													FROM LastFeedback
													ORDER BY topic, source';
									$stmt = $conn->prepare($sql);
									$stmt->execute();
									$feedback = $stmt->fetchAll(PDO::FETCH_ASSOC);
								}
								catch (PDOException $pe) {
									die("Could not connect to the database $db_name: " . $pe->getMessage());
								}

								foreach ($feedback as $row) {
									echo('<tr>');
									echo('<td>' . $row['topic'] . '</td>');
									echo('<td>' . $row['source'] . '</td>');
									echo('<td>' . $row['credit'] . '</td>');
									echo('</tr>');
								}
							?>
						</tbody>
					</table>
				</div>
			</div>
		</div>
		<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
		<!-- Include all compiled plugins (below), or include individual files as needed -->
		<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>
	</body>
</html>