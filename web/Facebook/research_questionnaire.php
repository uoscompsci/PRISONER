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
	}
	
	// Populate question info array if necessary.
	if (empty($_SESSION["question_info"])) {
		$question_info = array();
		$question_info[TYPE_PROFILE] = new QuestionType("Profile Info", TYPE_PROFILE, "User", "profile_data");	# We'll already have this info.
		$question_info[TYPE_PROFILE]->num_want = NUM_PROFILE_QUESTIONS;
		$question_info[TYPE_FRIEND] = new QuestionType("Friend Info", TYPE_FRIEND, "Friends", "friend_data");
		$question_info[TYPE_FRIEND]->num_want = NUM_FRIENDS_QUESTIONS;
		$question_info[TYPE_LIKE] = new QuestionType("Likes / Interests Info", TYPE_LIKE, NULL, "like_data");	# A collection of 3 different types.
		$question_info[TYPE_LIKE]->num_want = NUM_LIKES_QUESTIONS;
		$question_info[TYPE_CHECKIN] = new QuestionType("Check-in Info", TYPE_CHECKIN, "Checkin", "checkin_data");
		$question_info[TYPE_CHECKIN]->num_want = NUM_CHECKIN_QUESTIONS;
		$question_info[TYPE_STATUS] = new QuestionType("Status Update Info", TYPE_STATUS, "Status", "status_data");
		$question_info[TYPE_STATUS]->num_want = NUM_STATUS_QUESTIONS;
		$question_info[TYPE_ALBUM] = new QuestionType("Album Info", TYPE_ALBUM, "Album", "album_data");
		$question_info[TYPE_ALBUM]->num_want = NUM_PHOTO_ALBUM_QUESTIONS;
		$question_info[TYPE_PHOTO] = new QuestionType("Photo Info", TYPE_PHOTO, "Photo", "photo_data");
		$question_info[TYPE_PHOTO]->num_want = NUM_PHOTO_QUESTIONS;
		
		$_SESSION["question_info"] = $question_info;	# Question type data.
		$_SESSION["compensation_needed"] = 0;	# Number of extra questions we'll have to ask.
		$_SESSION["questions"] = array();	# Question objects.
	}
	
	// Retrieve info from session.
	$participant_id = $_SESSION["participant_id"];
	$participant_group = $_SESSION["group"];
	$study_title = $_SESSION["study_title"];
	$checked_for_restore = $_SESSION["checked_restore"];
	$prisoner_session_id = $_SESSION["prisoner_session_id"];
	$determined_all_questions = $_SESSION["determined_all_questions"];
	$question_num = $_SESSION["question_number"];
	$questions = &$_SESSION["questions"];
	
	// Load initial data.
	load_init_data($prisoner_session_id);
	$participant_fb_id = $_SESSION["question_info"][TYPE_PROFILE]->data["_id"];
	$enc_facebook_id = encrypt($participant_fb_id);	# Sensitive data is encrypted.
	$loaded_all_data = true;	# Will be set to false if necessary.
	
	// Check if this is a returning participant. (Do we need to restore their session?)
	if (!$checked_for_restore) {
		$query = "SELECT * FROM participant WHERE facebook_id = '$enc_facebook_id'";
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
			
			// Has this person already finished the study?
			$is_finished = $row["is_finished"];
			
			if ($is_finished) {
				$_SESSION["info_message"] = "<strong>you have already completed this study</strong>";
				log_msg("Notice: Screening participant out as they've already completed the study.");
				header("Location: " . SCREENED_OUT_URL);
			}
			
			else {
				// Restore the participant's session.
				$participant_session_data = $row["session_data"];
				$participant_session_data = $participant_session_data;
				$success = session_decode($participant_session_data);
				load_notice("Welcome back. We have restored your answers so you can pick up from where you left off.");
				log_msg("Session restored: " . $success);
					
				// Store the fact we checked for a restore and redirect. (To reload session)
				$_SESSION["checked_restore"] = true;
				header("Location: research_questionnaire.php");
			}
		}
		
		// This isn't a returner. Populate session with Facebook data and questions.
		else {
			// Link participant ID with Facebook ID. (Encrypted)
			$query = "UPDATE participant SET facebook_id = '$enc_facebook_id' WHERE id = '$participant_id'";
			$result = mysqli_query($db, $query);
			
			if (!$result) {
				log_msg("Error - Failed to link participant ID with Facebook ID: " . mysqli_error($db));
			}

			else {
				log_msg("Linked participant ID with Facebook ID.");
			}
			
			// Store the fact we checked for a restore.
			$_SESSION["checked_restore"] = true;
		}
	}
	
	// We still need to work out the questions we'll ask.
	if (count($questions) < NUM_QUESTIONS) {
		load_additional_data($prisoner_session_id);	# Rest of data not included in init.
		$questions_to_add = array();
		
		// For each type of question. (Profile, friends, interests...)
		foreach ($_SESSION["question_info"] as &$question_info_obj) {
			log_msg("Checking " . $question_info_obj->friendly_name . ".");
			
			// We've already loaded the data and generated questions.
			if ($question_info_obj->generated_questions) {
				log_msg(" - Questions already generated for this type.");
			}
			
			// Load data (If necessary) and generate questions.
			else {
				if (!$question_info_obj->loaded_data) {
					$data = check_data_availability($question_info_obj->prisoner_name, $prisoner_session_id);
					
					if ($data !== false) {
						log_msg(" - Data is now available.");
						$question_info_obj->data = $data["_objects"];
						$question_info_obj->loaded_data = true;
					}
					
					else {
						$loaded_all_data = false;
						log_msg(" - Data is not yet available.");
					}
				}
				
				if ($question_info_obj->loaded_data) {
					// Calculate new amount of compensation needed.
					$compensation_needed = &$_SESSION["compensation_needed"];
					$compensation_needed += calculate_available_data($question_info_obj->type);
					
					// Load new questions into the session.
					$new_questions = get_questions($question_info_obj->type);
					$questions_to_add = array_merge($questions_to_add, $new_questions);
				}
			}
			
			log_msg(" - Done.");
		}
		
		// Add any questions to the session.
		shuffle($questions_to_add);
		$questions = array_merge($questions, $questions_to_add);
		log_msg("Appending any new questions to session. (New size: " . count($_SESSION["questions"]) . ")");
	}
		
	// Once we've loaded all the data, check to make sure there's enough.
	if ($loaded_all_data) {
		$question_info = &$_SESSION["question_info"];
		$compensation_needed = &$_SESSION["compensation_needed"];
		$total_data_available = calculate_total_data();
		
		// Participant doesn't have enough data available.
		if ($total_data_available < NUM_QUESTIONS) {
			$_SESSION["info_message"] = "your Facebook profile does not contain enough information";
			log_msg("Notice: Screening participant out. Only " . calculate_total_data() . " pieces of data available.");
			header("Location: " . SCREENED_OUT_URL);
		}
		
		// Compensation is necessary.
		else if ($compensation_needed > 0) {
			log_msg("Data compensation is required. (Need " . $compensation_needed . " more items)");
			
			$num_question_types = count($_SESSION["question_info"]);
			$type_index = 0;
				
			for ($i = 0; $i < $compensation_needed; $i ++) {
				// Hit limit of category types, reset index.
				if ($type_index == $num_question_types) {
					$type_index = 0;
				}
					
				// If this info type has spare capacity, use it.
				if ($question_info[$type_index]->num_spare > 0) {
					$question_info[$type_index]->num_want += 1;
					$question_info[$type_index]->num_spare -= 1;
					log_msg("- Assigning extra from " . $question_info[$type_index]->friendly_name . ". (Will ask: " . $question_info[$type_index]->num_want .
					", New spare capacity: " . $question_info[$type_index]->num_spare . ")");
				}
			
				else {
					$i -= 1;
				}
					
				$type_index ++;
			}
			
			// Get the extra questions.
			$extra_questions = array();
			
			foreach ($question_info as &$question_info_obj) {
				$extra_questions = array_merge($extra_questions, get_questions($question_info_obj->type));
			}
			
			log_msg("Adding " . count($extra_questions) . " into session.");
			shuffle($extra_questions);
			$questions = array_merge($questions, $extra_questions);
		}
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
		log_msg("Question #" . $question_num . ": " . $response);
		
		// Increment question pointer.
		$question_num += 1;
		log_msg("Question ID detected. Decoded and set next to " . $question_num . ".");
		
		// Participant has answered all questions. Redirect to debriefing.
		if ($question_num > NUM_QUESTIONS) {
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
	
	// Check question availability.
	$question_available = true;
	$meta_redirect = NULL;
	
	if (empty($this_question)) {
		$meta_redirect = "<meta http-equiv='Refresh' content='10;url=research_questionnaire.php' />";
		$question_available = false;
	}
	
	// If the question exists.
	if ($question_available) {
		$response = $this_question->response;
		
		if ($response == true) {
			$check_yes = "checked='checked'";
		}
		
		else if ($response === false) {
			$check_no = "checked='checked'";
		}
		
		// Get the question's markup.
		$to_display = get_question_markup($this_question, $question_num);
	}
	
	else {
		
	}
	
	// Flush output buffers.
	ob_end_flush();
?>

<!DOCTYPE HTML>
<html>
	<head>
		<?php 
			include_once("prisoner.include.head.php");
			echo $meta_redirect;
		?>
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
								
								// Display any notices and the question.
								echo display_notice() . "\n";
								echo $to_display . "\n";
								
								// If there was a question...
								if ($question_available) {
									// Print out the yes / no options.
									echo "<div class='question'>" .
									"<p>Will you share this piece of information with us?</p>" . "\n" .
									"<label><input type='radio' name='agree_to_share' value='Y' id='agree_to_share_1'" . $check_yes . ">Yes</label>" . "\n" .
									"<label><input type='radio' name='agree_to_share' value='N' id='agree_to_share_0'" . $check_no . ">No</label>" . "\n" .
									"</div>" . "\n";
									
									// Include the question's ID.
									echo $question_id_field;
									
									// Inlcude next / previous buttons.
									echo "<div class='navigation'>" . "\n";
									$next_button_text = "Next Question";
									
									if ($question_num > 1) {
										echo "<ul><li><a href='research_questionnaire.php?previous=1'>Previous Question</a></li></ul>";
									}
									
									if ($question_num == NUM_QUESTIONS) {
										$next_button_text = "Finish Study";
									}
									
									echo "<div class='next_submit'><input name='submit' type='submit' value='" . $next_button_text . "'></div>" . "\n" .
									"</div>" . "\n";
								}
								
								// If there was no question, display the loading text.
								else {
									include_once("prisoner.include.loading.php");
								}
							
							?>
							
						</form>
						<div class="clear"></div>
					</div>
				</div>
			</div>
		</div>
	</body>
</html>