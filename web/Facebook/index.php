<!DOCTYPE HTML>

<?php
	
	// Start a session on the server.
	session_start();
	
	// Session / cache control.
	header("Cache-Control: max-age=" . $CACHE_STAY_ALIVE);
	
	// Include any required components.
	include_once("prisoner.authentication.php");
	include_once("prisoner.constants.php");
	include_once("prisoner.core.php");
	include_once("prisoner.database.php");
	include_once("prisoner.logging.php");
	
	// Participant info variables.
	$user_group = NULL;
	$wants_further_emails = NULL;
	$survey_title = "";
	$about_message = "";
	$checkbox_value = "";
	$email_validation_message = "";
	$email_address = "";
	
	// Check to see if this participant has already been assigned a group. (Eg: Pressed "Back")
	if (!empty($_SESSION["Group"])) {
		$user_group = $_SESSION["Group"];
		$wants_further_emails = $_SESSION["FurtherEmails"];
		$email_validation_message = $_SESSION["EmailValidationMessage"];
		$email_address = $_SESSION["EmailAddress"];
		$checkbox_value = "checked='checked'";
		log_msg("Participant has already been assigned a group - " . $user_group);
	}
	
	// If not, assign a group.
	else {
		$user_group = assign_group();
	}
	
	// Group 1.
	if ($user_group == GROUP_1) {
		$survey_title = $GROUP_1_TITLE;
		$about_message = $GROUP_1_ABOUT;
	}
	
	// Group 2.
	else {
		$survey_title = $GROUP_2_TITLE;
		$about_message = $GROUP_2_ABOUT;
	}
	
	// Save group info in session.
	$_SESSION["Group"] = $user_group;
	$_SESSION["Title"] = $survey_title;
	
?>

<html>
	<head>
		<?php include_once("prisoner.include.head.php"); ?>
		<title><?php echo $survey_title; ?> - Information - University Of St Andrews</title>
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
						<form name="participant_info" method="post" action="participation_consent.php">
							<h1><?php echo $survey_title; ?> - Survey Information</h1>
							
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