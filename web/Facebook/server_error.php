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
	$prisoner_session_id = $_SESSION["prisoner_session_id"];
	
	close_session($prisoner_session_id);
	session_destroy();
	
	// Flush output buffers.
	mysqli_close($db);
	ob_end_flush();
	
?>

<!DOCTYPE HTML>
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
						<div class="error_generic">
							<h1>Server Error</h1>
							<p>An error occurred that prevented us from making a session for you. Please <a href="index.php">click here</a> to try 
							again. <br />
							We apologise for any inconvenience.</p>
							<div class="clear"></div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</body>
</html>