<?php

	// Start a session on the server.
	ob_start();
	include_once("prisoner.classes.php");
	session_start();
	
	// Include any required components.
	include_once("prisoner.authentication.php");
	include_once("prisoner.constants.php");
	include_once("prisoner.core.php");
	include_once("prisoner.database.php");
	
	// Session / cache control.
	header("Cache-Control: max-age=" . CACHE_STAY_ALIVE);
		
	// Retrieve info from session.
	$user_group = $_SESSION["group"];
	$study_title = $_SESSION["study_title"];
	$info_message = $_SESSION["info_message"];
	
	// Flush output buffers.
	ob_end_flush();
?>

<!DOCTYPE HTML>
<html>
	<head>
		<?php include_once("prisoner.include.head.php"); ?>
		<title>Ethics In Online Social Network Research - University Of St Andrews</title>
	</head>
	
	<body>
		<div class="wrapper">
			<div class="content-container">
				<div class="content">
					<div class="info">
						<form name="participant_info" method="post" action="check_participation_consent.php">
							<h1>This Study Has Finished</h1>
							<p>Thank you for your interest in this research study. We do not need any more participants at this time.</p>
							<div class="clear"></div>
						</form>
					</div>
				</div>
			</div>
		</div>
	</body>
</html>