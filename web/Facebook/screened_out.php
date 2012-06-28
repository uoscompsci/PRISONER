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
	$user_group = $_SESSION["group"];
	$study_title = $_SESSION["study_title"];
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
							<h1>Screened Out</h1>
							<?php
								$msg = "Unfortunately we have had to screen you out of this study. This is because <strong>" .
								$info_message . "</strong>. Thank you for your interest in this research.";
								echo get_notice($msg, false);
							?>
							
							<div class="clear"></div>
						</form>
					</div>
				</div>
			</div>
		</div>
	</body>
</html>