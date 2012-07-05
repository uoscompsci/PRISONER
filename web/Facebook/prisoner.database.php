<?php

	// Include any required components.
	include_once("prisoner.constants.php");
	include_once("prisoner.core.php");
	
	
	// Try and connect to the database.
	$db = mysqli_connect(DATABASE_HOST, DATABASE_USER, DATABASE_PASS, DATABASE_NAME);
	
	// Connection error.
	if (!$db) {
		log_msg("Error - Couldn't connect to database server: " . mysqli_error());
	}
	
	// All good.
	else {
		log_msg("Successfully connected to database.");
	}
	
?>