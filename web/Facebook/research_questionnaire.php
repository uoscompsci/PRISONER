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
	
	// Retrieve info from session.
	set_session();
	$session_cookie = $_SESSION["PRISession_Cookie"];
	$user_group = $_SESSION["group"];
	$study_title = $_SESSION["study_title"];
	$question_num = $_SESSION["question_number"];
	$questions = $_SESSION["questions"];
	
	// Get participant's Facebook info if necessary.
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
	
	// Retrieve info from POST.
	$question_id = $_POST["question_id"];
	$question_num = NULL;
	
	// This is the participant's first question.
	// We don't want to do anything other than display the first question to them.
	if (empty($question_id)) {
		$question_num = 1;
		log_msg("No question ID detected, assuming first question.");
	}
	
	// Get the participant's response and display the next question.
	else {
		$question_num = str_replace(SALT, "", base64_decode($question_id));
		$question_num += 1;
		log_msg("Question ID detected. Decoded and set next to " . $question_num . ".");
		
		// Participant has answered all questions. Redirect to debriefing.
		if ($question_num > NUM_QUESIONS) {
			header("Location: " . DEBRIEFING_URL);
		}
	}
	
	// Encode question number for markup.
	$question_id = base64_encode(SALT . $question_num);
	$question_id_field = "<input type='hidden' name='question_id' id='question_id' value='" . $question_id . "'>";
	
	// Get the question. (Remember to -1 for the right index)
	$this_question = $questions[($question_num - 1)];
		
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
							
							<p><?php echo $to_display . "\n"; ?></p>
							
							<?php echo $question_id_field . "\n"; ?>
							<div class="next_submit">
								<input name="submit" type="submit" value="Next Question">
							</div>
							
							<div class="clear"></div>
						</form>
					</div>
				</div>
			</div>
		</div>
	</body>
</html>