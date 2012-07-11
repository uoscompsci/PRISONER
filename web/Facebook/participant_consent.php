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
		session_destroy();
		exit;
	}
		
	// Retrieve info about participant from session.
	$participant_group = $_SESSION["group"];
	$study_title = $_SESSION["study_title"];
	
	
	// Retrieve info from POST.
	$participant_wants_info = $_POST["store_email"];
	
	// Participant doesn't want follow-up emails.
	if (empty($participant_wants_info)) {
		log_msg("Participant does not want further emails.");
		$_SESSION["wants_further_emails"] = false;
	}
	
	// Participant wants further info.
	else {
		log_msg("Participant wants further emails.");
		$email_address = $_POST["email_address"];
		$_SESSION["wants_further_emails"] = true;
		$_SESSION["email_address"] = $email_address;
		
		// Email address doesn't validate.
		if (!preg_match(EMAIL_ADDRESS_REGEX, $email_address)) {
			$_SESSION["email_validation_message"] = "<strong>Error -</strong> Please enter a valid email address.";
			log_msg("Error - Email address failed validation.");
			header("Location: index.php#further_info");
		}
		
		// Email address ok.
		else {
			$_SESSION["email_validation_message"] = "";
			log_msg("Email address validated. Adding to mailing list.");
			
			// Encrypt email address and store in database.
			$enc_email_address = encrypt($email_address);
			$query = "INSERT INTO mailing_list (email_address) VALUES ('$enc_email_address')";
			$result = mysqli_query($db, $query);
			
			// Storing email address failed.
			if (!$result) {
				// Get the error number.
				$err_no = mysqli_errno($db);
				
				// Caused by email address already existing? Ignore. (Not really an error for us)
				if ($err_no = MYSQLI_ERROR_DUPLICATE) {
					log_msg("Email address already exists in database.");
				}
				
				// Log error.
				else {
					log_msg("Error - Failed to store email address: " . mysqli_error($db));
				}
			}
			
			// Stored email address.
			else {
				log_msg("Saved email address in database.");
			}
		}
	}
	
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
						<form name="participant_info" method="post" action="check_participation_consent.php">
							<h1><?php echo $study_title; ?> - Participation Consent Form</h1>

                            <p>The University of St Andrews attaches high priority to the ethical conduct of research.
                            The purpose of this page is to obtain your consent before you begin the study. Please read the entire page,
                            consider the points contained within, and if you consent to all of the terms of the study, then use
                            the "Next" button to begin.</p>

							<h2>1. Researcher(s) name(s)</h2>
							<p><a href="http://www.cs.st-andrews.ac.uk/~tristan/" target="_blank">Tristan Henderson</a>.</p>
							
							<h2>2. What is identifiable / attributable data?</h2>
							<p>‘Identifiable/Attributable data’ is data where the participant is identified, such as when a 
							public figure gives an interview, or where consent is given by a participant for their name (including 
							perhaps gender and address) to be used in the research outputs. 
							The raw data will be held confidentially by the researcher(s) (and supervisors), The published research 
							will clearly identify and attribute data collected to the participant.</p>
							
							<h2>3. Facebook app</h2>
							<p>If you choose to take part in this study, you will be asked to grant a Facebook app (named PRISONER) access to 
							your data. You will be unable to participate in the study if you do not authenticate the app.</p>
							
							<h2>4. Consent</h2>
							<p>The purpose of this form is to ensure that you are willing to take part in this study and to let 
							you understand what it entails. Signing this form does not commit you to anything you do not wish to do 
							and you are free to withdraw at any stage. <br />
							Please answer each statement concerning the collection and use of the research data.</p>
							
							<div class="consent_check">
								<table>
									<tr>
										<td class="consent_info">I have read and understood the information sheet.</td>
										<td>
											<label><input type="radio" name="read_info_sheet" value="1" id="read_info_sheet_1">Yes</label>
											<label><input type="radio" name="read_info_sheet" value="" id="read_info_sheet_0">No</label>
										</td>
									</tr>
									<tr>
										<td class="consent_info">I understand that I can withdraw from the study at any time without having to give an explanation.</td>
										<td>
											<label><input type="radio" name="understand_widthdraw" value="1" id="understand_widthdraw_1">Yes</label>
											<label><input type="radio" name="understand_widthdraw" value="" id="understand_widthdraw_0">No</label>
										</td>
									</tr>
									<tr>
										<td class="consent_info">I agree to being identified in any subsequent publications or use.</td>
										<td>
											<label><input type="radio" name="agree_identification" value="1" id="agree_identification_1">Yes</label>
											<label><input type="radio" name="agree_identification" value="" id="agree_identification_0">No</label>
										</td>
									</tr>
									<tr>
										<td class="consent_info">I understand that my raw data will be kept securely and will be accessible only to the researcher and 
										other researchers. I agree to all data collected being attributable to me and being identified as mine at 
										all times. I also understand that in the published research any contribution made by me may be clearly identified 
										and attributed as mine.</td>
										<td>
											<label><input type="radio" name="understand_data_storage" value="1" id="understand_data_storage_1">Yes</label>
											<label><input type="radio" name="understand_data_storage" value="" id="understand_data_storage_0">No</label>
										</td>
									</tr>
									<tr>
										<td class="consent_info">I agree to my data (in line with conditions outlined above) being kept by the researcher and being archived 
										and used for further research projects / by other bona fide researchers.</td>
										<td>
											<label><input type="radio" name="agree_info_keep" value="1" id="agree_info_keep_1">Yes</label>
											<label><input type="radio" name="agree_info_keep" value="" id="agree_info_keep_0">No</label>
										</td>
									</tr>
									<tr>
										<td class="consent_info">I have been made fully aware of the potential risks associated with this research and am satisfied with the 
										information provided.</td>
										<td>
											<label><input type="radio" name="aware_risks" value="1" id="aware_risks_1">Yes</label>
											<label><input type="radio" name="aware_risks" value="" id="aware_risks_0">No</label>
										</td>
									</tr>
									<tr>
										<td class="consent_info">I am over the age of 18.</td>
										<td>
											<label><input type="radio" name="over_18" value="1" id="over_18_1">Yes</label>
											<label><input type="radio" name="over_18" value="" id="over_18_0">No</label>
										</td>
									</tr>
									<tr>
										<td class="consent_info">I am a Facebook user.</td>
										<td>
											<label><input type="radio" name="facebook_user" value="1" id="facebook_user_1">Yes</label>
											<label><input type="radio" name="facebook_user" value="" id="facebook_user_0">No</label>
										</td>
									</tr>
									<tr>
										<td class="consent_info">I am a current university student.</td>
										<td>
											<label><input type="radio" name="is_student" value="1" id="is_student_1">Yes</label>
											<label><input type="radio" name="is_student" value="" id="is_student_0">No</label>
										</td>
									</tr>
									<tr>
										<td class="consent_info">I agree to take part in the study.</td>
										<td>
											<label><input type="radio" name="agree_participation" value="1" id="agree_participation_1">Yes</label>
											<label><input type="radio" name="agree_participation" value="" id="agree_participation_0">No</label>
										</td>
									</tr>
								</table>
							</div>
							
							<p>Participation in this research is completely voluntary and your consent is required before you can 
							participate in this research. If you decide at a later date that data should be destroyed you should 
							<a href="mailto:tnhh@st-andrews.ac.uk">contact us by e-mail</a>. If you have any questions prior to 
							beginning the study then you should also contact us by e-mail.</p>
							
							<div class="navigation">
								<ul><li><a href="index.php">Back</a></li></ul>
								
								<div class="next_submit">
									<input name="submit" type="submit" value="Next">
								</div>
							</div>
							
							<div class="clear"></div>
						</form>
					</div>
				</div>
			</div>
		</div>
	</body>
</html>
