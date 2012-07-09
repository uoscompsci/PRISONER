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
	
	// Should the participant be here?
	$can_view = assert_can_view(STAGE_CONSENT_PAGE);
	
	// No. Take them back to the index / landing page.
	if (!$can_view) {
		log_msg("Caught bad participant. Redirecting to landing page.");
		header("Location: index.php");
	}
	
	// Retrieve info from session.
	$study_title = $_SESSION["study_title"];
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
		$consent_info[] = $_POST["facebook_user"];
		$consent_info[] = $_POST["is_student"];
		$consent_info[] = $_POST["agree_participation"];
		
		// Default to true.
		$consent_granted = true;
		$_SESSION["participant_stage"] = STAGE_GIVEN_CONSENT;
		
		// Loop through consent info array and check values.
		foreach ($consent_info as $item) {
			// Participant must have agreed to ALL terms to continue.
			if (empty($item)) {
				$consent_granted = false;
				$_SESSION["participant_stage"] = STAGE_NO_CONSENT;
				$_SESSION["info_message"] = "<strong>either you are not eligible or you did not agree to the terms</strong>";
				log_msg("Notice: Screening participant out as they did not agree to the terms.");
				header("Location: " . SCREENED_OUT_URL);
				break;
			}
		}
	}
	
	// Consent was granted.
	if ($consent_granted) {
		$_SESSION["participant_consent"] = true;
		$participation_url = $_SESSION["participation_url"];	# From earlier.
		
		// Compose messages to display.
		$message_to_display = $STUDY_START_MESSAGE;
		$participation_link = "<div class='next_submit'><input name='submit' type='submit' value='Begin Study'></div>";
		
		log_msg("Consent granted by paricipant.");
	}
	
	else {
		$message_to_display = $NO_CONSENT_MESSAGE;
		log_msg("Participant did not agree to terms.");
	}
	
	// Flush output buffers.
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
						<h1>Thank You For Your Time</h1>
						<form name="participant_info" method="post" action="<?php echo $participation_url; ?>">
							<?php echo $message_to_display; echo $participation_link; ?>
						</form>		
						<div class="clear"></div>
					</div>
				</div>
			</div>
		</div>
	</body>
</html>