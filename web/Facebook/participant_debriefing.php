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
	$participant_group = $_SESSION["group"];
	$study_title = $_SESSION["study_title"];
	
?>

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
						<h1>Debriefing</h1>
						
						<h2>1. Your results</h2>
						<ul>
							<?php
								
								// Retrieve questions from session.
								$questions = $_SESSION["questions"];
								
								// Get info about questions and responses.
								$profile_question_info = get_question_meta_data(TYPE_PROFILE);
								$friend_question_info = get_question_meta_data(TYPE_FRIEND);
								$like_question_info = get_question_meta_data(TYPE_LIKE);
								$checkin_question_info = get_question_meta_data(TYPE_CHECKIN);
								$status_question_info = get_question_meta_data(TYPE_STATUS);
								$album_question_info = get_question_meta_data(TYPE_ALBUM);
								$photo_question_info = get_question_meta_data(TYPE_PHOTO);
								
								// Number of questions of each type.
								$num_profile_questions = $profile_question_info[0];
								$num_friend_questions = $friend_question_info[0];
								$num_like_questions = $like_question_info[0];
								$num_checkin_questions = $checkin_question_info[0];
								$num_status_questions = $status_question_info[0];
								$num_album_questions = $album_question_info[0];
								$num_photo_questions = $photo_question_info[0];
								
								// Shares of each type.
								$num_profile_shares = $profile_question_info[1];
								$num_friend_shares = $friend_question_info[1];
								$num_like_shares = $like_question_info[1];
								$num_checkin_shares = $checkin_question_info[1];
								$num_status_shares = $status_question_info[1];
								$num_album_shares = $album_question_info[1];
								$num_photo_shares = $photo_question_info[1];
								
								// Percentage shares.
								$percent_profile_shares = $profile_question_info[2];
								$percent_friend_shares = $friend_question_info[2];
								$percent_like_shares = $like_question_info[2];
								$percent_checkin_shares = $checkin_question_info[2];
								$percent_status_shares = $status_question_info[2];
								$percent_album_shares = $album_question_info[2];
								$percent_photo_shares = $photo_question_info[2];
								
								echo "<li>You were asked <strong>" . $num_profile_questions . "</strong> questions about your profile and " .
								"personal information and shared with us <strong>" . $num_profile_shares . "</strong> times. " .
								"(<strong>" . $percent_profile_shares . "%</strong>)</li>" . "\n";
								
								echo "<li>You were asked <strong>" . $num_friend_questions . "</strong> questions about your friends " .
								" and shared with us <strong>" . $num_friend_shares . "</strong> times. " .
								"(<strong>" . $percent_friend_shares . "%</strong>)</li>" . "\n";
								
								echo "<li>You were asked <strong>" . $num_like_questions . "</strong> questions about your likes and " .
								"interests and shared with us <strong>" . $num_like_shares . "</strong> times. " .
								"(<strong>" . $percent_like_shares . "%</strong>)</li>" . "\n";
								
								echo "<li>You were asked <strong>" . $num_checkin_questions . "</strong> questions about check-ins " .
								"and places you've been and shared with us <strong>" . $num_checkin_shares . "</strong> times. " .
								"(<strong>" . $percent_checkin_shares . "%</strong>)</li>" . "\n";
								
								echo "<li>You were asked <strong>" . $num_status_questions . "</strong> questions about status updates " .
								"you have posted and shared with us <strong>" . $num_status_shares . "</strong> times. " .
								"(<strong>" . $percent_status_shares . "%</strong>)</li>" . "\n";
								
								echo "<li>You were asked <strong>" . $num_album_questions . "</strong> questions about photo albums " .
								"you have uploaded and shared with us <strong>" . $num_album_shares . "</strong> times. " .
								"(<strong>" . $percent_album_shares . "%</strong>)</li>" . "\n";
								
								echo "<li>You were asked <strong>" . $num_photo_questions . "</strong> questions about photos of you " .
								"and shared with us <strong>" . $num_photo_shares . "</strong> times. " .
								"(<strong>" . $percent_photo_shares . "%</strong>)</li>" . "\n";
								
								// Commit results.
								commit_participant_results();
							?>
						</ul>
							
						<h2>2. Actual project title</h2>
						<p>Ethics in online social network research.</p>
							
						<h2>3. Researcher(s) name(s)</h2>
						<p>Tristan Henderson.</p>
							
						<h2>4. Nature of project</h2>
						<p>This research project was conducted to investigate ethical concerns in online social network research. 
						Lots of research projects, such as the project that you were just asked to participate in, use online 
						social network data. But there are many concerns about using such data, for instance privacy risks if sensitive 
						health data are leaked, or if knowledge about friendships are exposed. Some common examples include battered 
						spouses who might not want their spouses to be able to find them, but this might be possible if they were to 
						contact a friend of a friend, or employees who might not want their employers to see their after-work 
						activities on Facebook.</p>
							
						<p>To explore these issues we have asked you to share some of your online social network data with us. 
						We have deceived you into believing that you were participating in a research project about 
						<?php echo $study_title; ?>. This is an example of a real research project that has taken place in the recent past. 
						In actual fact we have not been investigating this, but rather we have been interested in what type of information you were 
						willing to share with us. We are not interested in the actual data themselves, and we have <strong>not</strong> stored 
						any of your social network data. The only information that we have stored is whether you were willing to share.</p>
							
						<p>It was necessary to deceive you because if we had explained that we were not storing any of your data, you may have 
						over-shared with us since the risks were minimal.</p>
							
						<p>From this research we hope to be able to create some guidelines for researchers who wish to use online social 
						network data. For instance, if there are particular types of data that participants seem very unwilling to share, then 
						researchers ought to determine ways of using other types of data rather than these.</p>
							
						<h2>5. Storage of data</h2>
						<p>As outlined in the Participant Information Sheet your data will now be retained for a period of 10 years before 
						being destroyed. <strong>But</strong> the only data that will be stored will be information about what types of data 
						you were willing to share. These will not be stored with any identifier indicating you. If you are unhappy with 
						this then you are free to withdraw your consent by <a href="mailto:tnhh@st-andrews.ac.uk">contacting us</a>. 
						Your data will remain accessible to only the researchers or it may be used for future scholarly purposes without further 
						contact or permission if you have given permission on the Consent Form.</p>
							
						<p>We will store your Facebook username in a separate database for the duration of the study. This is to prevent 
						participants from taking the study again. These usernames will not be associated with any of the data. We will also 
						use these usernames to contact you with details of your Amazon voucher. Once the study is complete, we will delete 
						these usernames, unless you have given us consent to store your details to contact you when papers about the study 
						are made available.</p>
							
						<h2>6. What should I do if I have concerns about this study?</h2>
						<p>If you have any concerns about the procedures used in this study, or would like to know any more information about 
						the methods used or this area of research, then please contact the researchers using the details below. A full outline 
						of the procedures governed by the University Teaching and Research Ethical Committee are outlined on their 
						website <a href="http://www.st-andrews.ac.uk/utrec/complaints/" target="_blank">http://www.st-andrews.ac.uk/utrec/complaints/</a></p>
							
						<h2>7. Contact details</h2>
						<p>Researcher: Dr Tristan Henderson <br />
						Email: <a href="mailto:tnhh@st-andrews.ac.uk">tnhh@st-andrews.ac.uk</a><br />
						Phone: 01334 461637</p>
							
						<div class="clear"></div>
					</div>
				</div>
			</div>
		</div>
	</body>
</html>