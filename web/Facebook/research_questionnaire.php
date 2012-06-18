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
	include_once("prisoner.questionnaire.php");
	
	// Retrieve info from session.
	set_session();	# Retrieve info from PRISONER.
	$session_cookie = $_SESSION["PRISession_Cookie"];
	$user_group = $_SESSION["Group"];
	$study_title = $_SESSION["Title"];
	$question_num = 1;
	
	// Get participant's Facebook info.
	get_facebook_data($session_cookie);
	$enough_info = calculate_num_info_types();
	
	if ($enough_info == false) {
		$_SESSION["info_message"] = "<strong>your Facebook profile does not contain enough information.</strong>";
		header("Location: " . SCREENED_OUT_URL);
	}
	
	$profile_info = $_SESSION["profile_info"];
	$likes_info = $_SESSION["likes_info"];
	$friends_info = $_SESSION["friends_list"];
	$checkin_info = $_SESSION["checkin_info"];
	$status_update_info = $_SESSION["status_update_info"];
	
	$to_display = "Your name is <strong>" . $profile_info["_firstName"] . "</strong> and you are " . $profile_info["_relationshipStatus"] . ".";
	
	if ($question_num >= NUM_QUESIONS) {
		//header("Location: " . DEBRIEFING_URL);
	}
		
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
							
							<p><?php echo $to_display; ?></p>
							
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