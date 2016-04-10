<?php 
require_once('connect.inc.php');
date_default_timezone_set('Europe/London');
session_start();
function updateSession(){
	if (isset($_SESSION['LAST_ACTIVITY']) && (time() - $_SESSION['LAST_ACTIVITY'] > 1800)) {
		// last request was more than 30 minutes ago (although sessions die after 24 anyway)
		destroySession();
		newSession();
	}
	$_SESSION['LAST_ACTIVITY'] = time(); // update last activity time stamp
}
function destroySession(){
	session_unset(); // unset $_SESSION variable for the run-time 
	//session_destroy(); // destroy session data in storage
}
function newSession(){
	session_regenerate_id();
}
?>