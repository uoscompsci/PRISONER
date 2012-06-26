<!DOCTYPE HTML>

<?php
	
	// Include any required components.
	include_once("prisoner.authentication.php");
	include_once("prisoner.classes.php");
	include_once("prisoner.constants.php");
	include_once("prisoner.core.php");
	include_once("prisoner.database.php");
	include_once("prisoner.questionnaire.php");
	
	// Start a session on the server.
	session_start();
	
	// Session / cache control.
	header("Cache-Control: max-age=" . CACHE_STAY_ALIVE);
	
	// Should the participant be here?
	$can_view = assert_can_view(STAGE_GIVEN_CONSENT);
	
	// No. Take them back to the index / landing page.
	if (!$can_view) {
		log_msg("Caught bad participant. Redirecting to landing page.");
		header("Location: index.php");
	}
	
	// Retrieve info from session.
	set_session();
	$participant_id = $_SESSION["participant_id"];
	$participant_group = $_SESSION["group"];
	$session_cookie = $_SESSION["PRISession_Cookie"];
	$study_title = $_SESSION["study_title"];
	$checked_for_restore = $_SESSION["checked_restore"];
	$question_num = $_SESSION["question_number"];
	$questions = $_SESSION["questions"];
	
	// Load the participant's profile information into the session and get their Facebook ID.
	load_profile_info($session_cookie);	
	$participant_fb_id = $_SESSION["profile_info"]["_id"];
	
	// Check if this is a returning participant. (Do we need to restore their session?)
	if (!$checked_for_restore) {
		$query = "SELECT * FROM participant WHERE facebook_id = '$participant_fb_id'";
		$result = mysqli_query($db, $query);
		$row = mysqli_fetch_array($result);

		// This participant is a returner.
		if (mysqli_num_rows($result) >= 1) {
			log_msg("Detected returning participant. Attempting to restore session.");
			$query = "DELETE FROM participant WHERE id = '$participant_id'";
			$result = mysqli_query($db, $query);
				
			if (!$result) {
				log_msg("Error - Failed to delete redundant participant data: " . mysqli_error($db));
			}
				
			else {
				log_msg("Removed old data ok.");
			}
			
			// Restore the participant's session.
			$participant_session_data = $row["session_data"];
			$success = session_decode($participant_session_data);
			log_msg("Session restored: " . $success);
			
			// Store the fact we checked for a restore and redirect. (To reload session)
			$_SESSION["checked_restore"] = true;
			header("Location: research_questionnaire.php");
		}
		
		// This isn't a returner. Populate session with Facebook data and questions.
		else {
			// Link participant ID with Facebook ID.
			$query = "UPDATE participant SET facebook_id = '$participant_fb_id' WHERE id = '$participant_id'";
			$result = mysqli_query($db, $query);
			
			if (!$result) {
				log_msg("Error - Failed to link participant ID with Facebook ID: " . mysqli_error($db));
			}

			else {
				log_msg("Linked participant ID with Facebook ID.");
			}
			
			// Load Facebook data and questions.
			get_facebook_data($session_cookie);
			$num_questions_per_type = calculate_num_info_types();
		
			// Profile does not contain enough info for the study. Screen out.
			if (!$num_questions_per_type) {
				$_SESSION["info_message"] = "<strong>your Facebook profile does not contain enough information.</strong>";
				header("Location: " . SCREENED_OUT_URL);
			}
		
			// Generate questions if necessary.
			else {
				if (empty($_SESSION["questions"])) {
					$questions = generate_questions($num_questions_per_type);
					$_SESSION["questions"] = $questions;
				}
			}
		}
		
		// Store the fact we checked for a restore.
		$_SESSION["checked_restore"] = true;
	}
	
	// Save current session state in database.
	$session_str = mysqli_real_escape_string($db, session_encode());
	$query = "UPDATE participant SET session_data = '$session_str' WHERE id = '$participant_id'";
	$result = mysqli_query($db, $query);
		
	if (!$result) {
		log_msg("Error - Failed to store current state: " . mysqli_error($db));
	}
		
	else {
		log_msg("State saved successfully.");
	}
	
	// Retrieve info from POST.
	$question_id = NULL;
	$question_num = NULL;
	
	// If there's a question ID in POST, decode it and grab the response.
	if (!empty($_POST["question_id"])) {
		$question_id = $_POST["question_id"];
		$question_num = str_replace(SALT, "", base64_decode($question_id));
		$response = NULL;
		$agree_to_share = $_POST["agree_to_share"];
		
		// Shared.
		if ($agree_to_share == "Y") {
			$_SESSION["notice"] = "";
			$response = true;
		}
		
		// Not shared.
		else if ($agree_to_share == "N") {
			$_SESSION["notice"] = "";
			$response = false;
		}
		
		// Not filled in.
		else {
			load_notice("You must indicate whether or not you would share this information with us before continuing.");
			$question_num -= 1;	# So participant is forced to complete same question again.
		}
		
		// Store response in session.
		$questions[($question_num - 1)]->response = $response;
		$_SESSION["questions"] = $questions;
		log_msg("Question #" . $question_num . ": " . $response);
		
		// Increment question pointer.
		$question_num += 1;
		log_msg("Question ID detected. Decoded and set next to " . $question_num . ".");
		
		// Participant has answered all questions. Redirect to debriefing.
		if ($question_num > NUM_QUESIONS) {
			header("Location: " . DEBRIEFING_URL);
		}
	}
	
	// If there's no info in POST, there may be an ID in the session. (From restore)
	else if (!empty($_SESSION["question_id"])) {
		$question_id = $_SESSION["question_id"];
		$question_num = str_replace(SALT, "", base64_decode($question_id));
		log_msg("Question ID retrieved from session. (#" . $question_num . ")");
	}
	
	// This is the participant's first question.
	// We don't want to do anything other than display the first question to them.
	else {
		$question_num = 1;
		log_msg("No question ID detected, assuming first question.");
	}
	
	// Did the participant want the previous question?
	if ($_GET["previous"]) {
		if ($question_num > 1) {
			$question_num -= 1;
		}
	}
	
	// Encode question number and previous question number.
	$question_id = base64_encode(SALT . $question_num);
	$question_id_field = "<input type='hidden' name='question_id' id='question_id' value='" . $question_id . "'>";
	$_SESSION["question_id"] = $question_id;
	
	// Get the question. (Remember to -1 for the right index)
	$check_no = NULL;
	$check_yes = NULL;
	$this_question = $questions[($question_num - 1)];
	$response = $this_question->response;
	
	if ($response == true) {
		$check_yes = "checked='checked'";
	}
	
	else if ($response === false) {
		$check_no = "checked='checked'";
	}
		
	// Get the question's markup.
	$to_display = get_question_markup($this_question, $question_num);
		
?>

<html>
	<head>
		<?php include_once("prisoner.include.head.php"); ?>
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
						
						<form name="questionnaire" method="post" action="research_questionnaire.php">
							<h1><?php echo $study_title; ?></h1>
							
							<?php
								
								echo get_notice();
								echo $to_display . "\n";
								 
							?>
							
							<div class="question">
								<p>Would you be willing to share this piece of information with us?</p>
								<label><input type="radio" name="agree_to_share" value="Y" id="agree_to_share_1" <?php echo $check_yes; ?>>Yes</label>
								<label><input type="radio" name="agree_to_share" value="N" id="agree_to_share_0" <?php echo $check_no; ?>>No</label>
							</div>
							
							<?php echo $question_id_field . "\n"; ?>
							
							<div class="navigation">
								<?php
									// If this isn't the first question, display the "Previous" link.
									if ($question_num > 1) { echo "<ul><li><a href='research_questionnaire.php?previous=1'>Previous Question</a></li></ul>"; }
								?>
								<div class="next_submit"><input name="submit" type="submit" value="Next Question"></div>
							</div>
							
							
						</form>
						<div class="clear"></div>
					</div>
				</div>
			</div>
		</div>
	</body>
</html>