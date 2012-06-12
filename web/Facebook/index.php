<?php
	
	// Start a session on the server.
	session_start();
	
	// Include any required components.
	include_once("prisoner.authentication.php");
	
	// Create a new PRISONER session and grab the results.
	$session_results = start_prisoner_session();
	$session_id = $session_results[0];
	$participation_url = $session_results[1];
	
	// Print info to the web page.
	echo "<h1>PRISONER - Hello World</h1>" .
	"<p>This is a 'Hello World' example to demonstrate PRISONER's Facebook gateway. <br />" .
	"To get started, you'll need to click <a href='" . $participation_url . "' title='Get started'>here</a> and sign in to Facebook.</p>";
	
?>