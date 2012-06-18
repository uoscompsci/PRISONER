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
	$user_group = $_SESSION["Group"];
	$study_title = $_SESSION["Title"];
	
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
						<form name="participant_info" method="post" action="check_participation_consent.php">
							<h1><?php echo $study_title; ?> - Debriefing</h1>
							
							<h2>1. Actual project title</h2>
							<p>Ethics in online social network research.</p>
							
							<h2>2. Researcher(s) name(s)</h2>
							<p>Tristan Henderson.</p>
							
							<h2>3. Nature of project</h2>
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
							
							<h2>4. Storage of data</h2>
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
							
							<h2>5. What should I do if I have concerns about this study?</h2>
							<p>If you have any concerns about the procedures used in this study, or would like to know any more information about 
							the methods used or this area of research, then please contact the researchers using the details below. A full outline 
							of the procedures governed by the University Teaching and Research Ethical Committee are outlined on their 
							website <a href="http://www.st-andrews.ac.uk/utrec/complaints/" target="_blank">http://www.st-andrews.ac.uk/utrec/complaints/</a></p>
							
							<h2>6. Contact details</h2>
							<p>Researcher: Dr Tristan Henderson <br />
							Email: <a href="mailto:tnhh@st-andrews.ac.uk">tnhh@st-andrews.ac.uk</a><br />
							Phone: 01334 461637</p>
							
							<div class="clear"></div>
						</form>
					</div>
				</div>
			</div>
		</div>
	</body>
</html>