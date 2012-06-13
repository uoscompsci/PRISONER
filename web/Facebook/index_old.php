<?php
	
	// Start a session on the server.
	session_start();
	
	// Include any required components.
	include_once("prisoner.authentication.php");
	
	// Create a new PRISONER session and grab the results.
	$session_results = start_prisoner_session();
	$session_id = $session_results[0];
	$participation_url = $session_results[1];
	
?>

<!DOCTYPE HTML>
<html>
	<head>
		<?php include_once("prisoner.include.head.php"); ?>
		<title>PRISONER - Hello World Example</title>
	</head>
	
	<body>
		<div class="wrapper">
			<div class="content">
				<h1>PRISONER - Hello World</h1>
				<p>This is a 'Hello World' example to demonstrate PRISONER's Facebook gateway. <br />
				To get started, click <a href="<?php echo $participation_url; ?>" title="Get started">here</a>.</p>
			</div>
		</div>
	</body>
</html>