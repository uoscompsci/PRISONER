<?php

	// Start a session on the server.
	ob_start();
	include_once("prisoner.classes.php");
	session_start();

	// Include any required components.
	include_once("prisoner.authentication.php");
	include_once("prisoner.classes.php");
	include_once("prisoner.constants.php");
	include_once("prisoner.core.php");
	include_once("prisoner.database.php");
	include_once("prisoner.questionnaire.php");
	
	// Session / cache control.
	header("Cache-Control: max-age=" . CACHE_STAY_ALIVE);
	
	// Should the participant be here?
	$can_view = assert_can_view(STAGE_GIVEN_CONSENT);
	
	// No. Take them back to the index / landing page.
	if (!$can_view) {
		log_msg("Caught bad participant. Redirecting to landing page.");
		header("Location: index.php");
		session_destroy();
		exit;
	}
	
	// Retrieve info from session.
	$participant_id = $_SESSION["participant_id"];
	$participant_group = $_SESSION["group"];
	$study_title = $_SESSION["study_title"];
	
	// Flush output buffers.
	mysqli_close($db);
	ob_end_flush();
	
?>

<!DOCTYPE HTML>
<html>
	<head>
		<?php include_once("prisoner.include.head.php"); ?>
		<meta http-equiv="Refresh" content="1; url=research_questionnaire.php" />
		<title><?php echo $study_title; ?> - University Of St Andrews</title>
	</head>
	
	<body>
		<script type="text/javascript">
			$(document).ready(function(){
			});
		</script>
		<div class="wrapper">
			<div class="content-container">
				<div class="content">
					<div class="info">
						<h1><?php echo $study_title; ?></h1>
						<?php include_once("prisoner.include.loading.php"); ?>
						<div class="clear"></div>
					</div>
				</div>
			</div>
		</div>
	</body>
</html>