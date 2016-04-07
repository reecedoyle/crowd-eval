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
			if ($_SERVER["REQUEST_METHOD"] == "POST") { // TODO add elastic search stuff in here too
				$ucl = $_POST['UCL'];
				$duck = $_POST['DuckDuckGo'];
				$topic = $_POST['topic'];
				$ranker = "";
				if ($ucl > $duck) {
					$ranker = "UCL";
				}
				if ($duck > $ucl) {
					$ranker = "DuckDuckGo";
				}
				echo '<script type="text/javascript">console.log("UCL: '.$ucl.'");</script>';
				echo '<script type="text/javascript">console.log("Duck: '.$duck.'");</script>';
				echo '<script type="text/javascript">console.log("Ranker: '.$ranker.'");</script>';
				if(!empty($ranker)){
					try {
						$conn = new PDO("mysql:host=$db_host;dbname=$db_name;charset=utf8mb4", $db_user, $db_pass);
						$sql = 'INSERT INTO Feedback
										(source, topic, credit) VALUES (:ranker, :topic, 1)
										ON DUPLICATE KEY
										UPDATE
										credit = (@cur_credit := credit) + 1';
						$stmt = $conn->prepare($sql);
						$stmt->bindParam(':ranker', $ranker);
						$stmt->bindParam(':topic', $topic);
						$stmt->execute();
					}
					catch (PDOException $pe) {
						die("Could not connect to the database $db_name: " . $pe->getMessage());
					}
				}
				echo '<script>window.location.replace("eval.php");</script>';
			}
			else{
				echo '<script>window.location.replace("/");</script>';
			}
		?>
	</body>
</html>