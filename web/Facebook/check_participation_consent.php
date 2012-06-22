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
	$survey_title = $_SESSION["study_title"];
	$participant_wants_info = $_SESSION["wants_further_emails"];
	$consent_granted = $_SESSION["participant_consent"];
	
	// Variables for later.
	$prisoner_session_id = NULL;
	$participation_url = NULL;
	$message_to_display = NULL;
	$participation_link = NULL;
		
	// If consent hasn't yet been granted, check it.
	if (empty($consent_granted)) {
		// Get consent info from POST.
		$consent_info = array();
		$consent_info[] = $_POST["read_info_sheet"];
		$consent_info[] = $_POST["understand_widthdraw"];
		$consent_info[] = $_POST["agree_identification"];
		$consent_info[] = $_POST["understand_data_storage"];
		$consent_info[] = $_POST["agree_info_keep"];
		$consent_info[] = $_POST["aware_risks"];
		$consent_info[] = $_POST["over_18"];
		$consent_info[] = $_POST["agree_participation"];
		
		// Default to true.
		$consent_granted = true;
		
		// Loop through consent info array and check values.
		foreach ($consent_info as $item) {
			// Participant must have agreed to ALL terms to continue.
			if (empty($item)) {
				$consent_granted = false;
				break;
			}
		}
	}
	
	// If the user gave consent, create a session with PRISONER.
	if ($consent_granted) {
		// Set session info and start PRISONER.
		$_SESSION["participant_consent"] = true;
		$session_results = start_prisoner_session();
		$prisoner_session_id = $session_results[0];
		$participation_url = $session_results[1];
		
		// Compose messages to display.
		$message_to_display = $STUDY_START_MESSAGE;
		$participation_link = "<div class='button_green'>" . "\n" .
		"<a href='" . $participation_url . "'>Begin</a>" . "\n" .
		"</div>";
		
		log_msg("Consent granted by paricipant.");
	}
	
	else {
		$message_to_display = $NO_CONSENT_MESSAGE;
		log_msg("Participant did not agree to terms.");
	}
	
?>

<html>
	<head>
		<?php include_once("prisoner.include.head.php"); ?>
		<title><?php echo $survey_title; ?> - University Of St Andrews</title>
	</head>
	
	<body>
		<div class="wrapper">
			<div class="content-container">
				<div class="content">
					<div class="info">
						<h1>Thank You For Your Time</h1>
						<?php echo $message_to_display; echo $participation_link; ?>							
						<div class="clear"></div>
					</div>
				</div>
			</div>
		</div>
	</body>
</html>