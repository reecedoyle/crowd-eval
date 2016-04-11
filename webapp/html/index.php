<?php 
	require_once('../inc/functions.php');
	updateSession();
?>
<html>
	<head>
		<title>Crowd Eval</title>
		<link rel='shortcut icon' href='favicon.ico' type='image/x-icon'/ >
		<link rel="stylesheet" type="text/css" href="css/reset.css">
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
		<link href='http://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,400,300,600,700' rel='stylesheet' type='text/css'>	
		<link href="css/cover.css" rel="stylesheet">
	</head>
	<body>
		<div class="site-wrapper">
			<div class="site-wrapper-inner">
				<div class="cover-container">
					<div class="masthead clearfix">
						<div class="inner">
							<h3 class="masthead-brand">CrowdEval</h3>
							<nav>
								<ul class="nav masthead-nav">
									<li class="active"><a href="#">Home</a></li>
									<li><a href="/eval.php">Evaluate</a></li>
									<li><a href="/learn-more.php">Learn More</a></li>
								</ul>
							</nav>
						</div>
					</div>
					<div class="inner cover">
						<h1 class="cover-heading">Welcome!</h1>
						<p class="lead">This is the homepage for the Information Retrieval and Data Mining group project of Reece Doyle, Richard Haar and Kapileshwar Syamasundar.</p>
						<p class="lead">
							<a href="/eval.php" class="btn btn-lg btn-success">Let's Evaluate!</a>
						</p>
						<p class="lead"><small>(though we recommend you <a href="/learn-more.php">learn more</a> before participating)</small></p>
					</div>
				</div>
			</div>
		</div>
		<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>
	</body>
</html>