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
	
	// Start a PRISONER session.
	$session_results = start_prisoner_session();
	$prisoner_session_id = $session_results[0];
	$participation_url = $session_results[1];
	$prisoner_participant_id = $session_results[2];
	$_SESSION["prisoner_session_id"] = $prisoner_session_id;	# This needs to be used for requests.
	$_SESSION["participation_url"] = $participation_url;	# We'll need this later.
	$_SESSION["prisoner_participant_id"] = $prisoner_participant_id;	# We'll need this later.
	
	// Participant info.
	$participant_id = NULL;
	$participant_group = NULL;
	$wants_further_emails = NULL;	# Not saved with participant data.
	
	// Study content.
	$study_title = NULL;
	$about_message = NULL;
	
	// Markup info.
	$checkbox_value = NULL;
	$email_validation_message = NULL;
	$email_address = NULL;
	
	
	// New participant! Assign them an ID and group.
	if (empty($_SESSION["participant_id"])) {
		$participant_id = $prisoner_session_id;
		$participant_group = assign_group();
		
		// Get the title for the study.
		if ($participant_group == GROUP_1) {
			$study_title = $GROUP_1_TITLE;
			$about_message = $GROUP_1_ABOUT;
		}
		
		else {
			$study_title = $GROUP_2_TITLE;
			$about_message = $GROUP_2_ABOUT;
		}
		
		// Save this info in session.
		$_SESSION["participant_id"] = $participant_id;
		$_SESSION["group"] = $participant_group;
		$_SESSION["study_title"] = $study_title;
		$_SESSION["participant_stage"] = STAGE_CONSENT_PAGE;	# Next stop.
		
		log_msg("Created new participant.");
		log_msg(" - ID set to: " . $participant_id);
		log_msg(" - Group set to: " . $participant_group);
		
		// Create a database entry for the new participant.
		$query = "INSERT INTO participant (id, group_id) VALUES ('$participant_id', $participant_group)";
		$result = mysqli_query($db, $query);
			
		// Storing participant info failed.
		if (!$result) {
			log_msg("Error - Failed to store participant info: " . mysqli_error($db));
		}
			
		// Success.
		else {
			log_msg("Saved participant info in database.");
		}
	}
	
	// This participant has been here before. Query session for their info.
	else {
		$participant_id = $_SESSION["participant_id"];
		$participant_group = $_SESSION["group"];
		$wants_further_emails = $_SESSION["wants_further_emails"];
		$email_validation_message = $_SESSION["email_validation_message"];
		$email_address = $_SESSION["email_address"];
		$study_title = $_SESSION["study_title"];
		
		if ($wants_further_emails) {
			$checkbox_value = "checked='checked'";
		}
		
		log_msg("Detected participant " . $participant_id . ".");
		log_msg(" - Group: " . $participant_group);
		
		// Get the about message.
		if ($participant_group == GROUP_1) {
			$about_message = $GROUP_1_ABOUT;
		}
		
		else {
			$about_message = $GROUP_2_ABOUT;
		}
	}
	
?>

<html>
	<head>
		<?php include_once("prisoner.include.head.php"); ?>
		<title><?php echo $study_title; ?> - Information - University Of St Andrews</title>
	</head>
	
	<body>
		<script type="text/javascript">
			$(document).ready(function(){
				// Hide the email input div if it isn't checked. (Eg: On page load)
				if (!$("#store_email").attr("checked")) {
					$(".email_input").hide();
				}
				
				// When the "Want further info" checkbox is checked, display the input div.
				$("#store_email").click(function(){
					if (this.checked) {
						$(".email_input").fadeIn(250);
					}
					else {
						$(".email_input").fadeOut(200);
					}
				});
				
				// Visual feedback.
				$("#email_address").focusin(function() {
					$(this).css("border-color","#666666");

				});
				
				// Visual feedback.
				$("#email_address").focusout(function() {
					$(this).css("border-color","#999999");
				});

			});
		</script>
		<div class="wrapper">
			<div class="content-container">
				<div class="content">
					<div class="info">
						<form name="participant_info" method="post" action="participant_consent.php">
							<h1><?php echo $study_title; ?> - Information</h1>
							
							<h2>1. What is the study about?</h2>
							<p><?php echo $about_message; ?> <br />
							This study is being conducted as part of my research in the <a href="http://www.cs.st-andrews.ac.uk/" target="_blank">School 
							of Computer Science</a>.</p>
						
							<h2>2. Do I have to take part?</h2>
							<p>Participation is completely voluntary. You should read the information on this page and then decide 
							whether or not to take part. If you do decide to take part you will be free to withdraw at any 
							time without providing a reason. You can do so by closing your web browser. 
							All of your personal data will then be deleted.</p>
						
							<h2>3. What would I be required to do?</h2>
							<p>You will be asked to complete a questionnaire in your browser. We anticipate that this will 
							take 30 minutes to complete. You will be presented with data from your Facebook social network that we 
							require for our research. You will then be asked whether you are willing to share these data with us. 
							It is completely up to you whether to share your data with us or not. If you do agree, then your data 
							will be stored and processed for the purposes of our research.</p>
						
							<h2>4. Will my participation be anonymous and confidential?</h2>
							<p>For the purposes of our research, we need to know your name and institution (e.g., university attended). 
							We would also like to have similar information for other members of your social network. It is up to you 
							whether to share these data or not. <br />
							All data will be stored by the researcher in a secure fashion. We would like to share these data with 
							other researchers to be used for future scholarly purposes. Again, this is up to you. You should 
							indicate whether you are willing to do so in the following questionnaire.</p>
						
							<h2>5. Storage and destruction of data collected</h2>
							<p>The data we collect will be accessible by the researcher(s) and supervisor(s) involved in this study only, 
							unless explicit consent for wider access is given by means of the consent form. Your data will be stored 
							for a period of at least 10 years before being destroyed, in an unanonymised format on a secure server in 
							our University.</p>
						
							<h2><a id="further_info">6. What will happen to the results of the research study?</a></h2>
							<p>We expect to have the results of this study ready by the end of 2012. They will be published in various 
							journal papers. If you wish to know more about the research or have copies of the papers sent to you, then please 
							indicate this here.</p>
							
							<div class="further_info_check">
								<input type="checkbox" name="store_email" id="store_email" <?php echo $checkbox_value; ?>>
								<label for="store_email">I wish to know more about this research</label>
							</div>
							<div class="email_input">
								<label for="email_address">Email address: </label>
								<input type="text" name="email_address" id="email_address" value="<?php echo $email_address; ?>">
								<label class="error_message" for="email_address"><?php echo $email_validation_message; ?></label>
							</div>
						
							<h2>7. Reward</h2>
							<p>You will receive a £5 Amazon.co.uk gift voucher for successfully completing this survey.</p>
						
							<h2>8. Are there any potential risks to taking part?</h2>
							<p>The risks of taking part involve sharing your online social network data with us. As part of the questionnaire, 
							you will tell us what data you are willing to share. This gives you the ability to manage these risks. If there are 
							any data that you do not wish to share, then please indicate as such in the questionnaire.</p>
						
							<h2>9. Consent and approval</h2>
							<p>This research proposal has been scrutinised and been granted Ethical Approval through the University ethical 
							approval process.</p>
						
							<h2>10. What should I do if I have concerns about this study?</h2>
							<p>A full outline of the procedures governed by the University Teaching and Research Ethical Committee is 
							available at 
							<a href="http://www.st-andrews.ac.uk/utrec/complaints/" target="_blank">http://www.st-andrews.ac.uk/utrec/complaints/</a></p>
						
							<h2>11. Contact details</h2>
							<p>Researcher: Dr Tristan Henderson <br />
							Email: <a href="mailto:tnhh@st-andrews.ac.uk">tnhh@st-andrews.ac.uk</a><br />
							Phone: 01334 461637</p>
							
							<div class="next_submit">
								<input name="submit" type="submit" value="Next">
							</div>
							
							<div class="clear"></div>
						</form>
					</div>
				</div>
			</div>
		</div>
	</body>
</html>