<!DOCTYPE HTML>

<?php

	// Start a session on the server.
	session_start();
	
	// Session / cache control.
	header("Cache-Control: max-age=" . CACHE_STAY_ALIVE);
	
	// Include any required components.
	include_once("prisoner.authentication.php");
	include_once("prisoner.constants.php");
	include_once("prisoner.core.php");
	include_once("prisoner.database.php");
		
	// Retrieve info from session.
	$user_group = $_SESSION["Group"];
	$study_title = $_SESSION["Title"];
	$info_message = $_SESSION["info_message"];
	
?>

<html>
	<head>
		<?php include_once("prisoner.include.head.php"); ?>
		<title><?php echo $study_title; ?> - University Of St Andrews</title>
	</head>
	
	<body>
		<div class="wrapper">
			<div class="content-container">
				<div class="content">
					<div class="info">
						<form name="participant_info" method="post" action="check_participation_consent.php">
							<h1><?php echo $study_title; ?> - Screened Out</h1>
							<p>Unfortunately we have had to screen you out of this study. The reason for this is because 
							<?php echo $info_message; ?> <br />
							Thank you for your interest in this research.</p>
							
							<div class="clear"></div>
						</form>
					</div>
				</div>
			</div>
		</div>
	</body>
</html>