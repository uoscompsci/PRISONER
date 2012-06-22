<?php
	
	// Start a session on the server.
	session_start();
	
	// Include any required components.
	include_once("prisoner.authentication.php");
	
	// Create a new PRISONER session and grab the results.
	$session_results = start_prisoner_session();
	$session_id = $session_results[0];
	$participation_url = $session_results[1];
	
	// Retrieve info from session.
	$user_group = $_SESSION["Group"];
	$survey_title = $_SESSION["Title"];
	$participant_wants_info = $_SESSION["FurtherEmails"];
	$consent = $_SESSION["Consent"];
	
?>

<html>
	<head>
		<?php include_once("prisoner.include.head.php"); ?>
		<title><?php echo $survey_title; ?> - University Of St Andrews</title>
	</head>
	
	<body>
		<div class="wrapper">
			<div class="content-container">
				<div class="content">
					<div class="info">
						<form name="participant_info" method="post" action="check_participation_consent.php">
							<h1>Thank You For Your Time</h1>
							<p>Unfortunately you cannot participate in this study if you do not agree to the terms on the consent page. <br />
							No information has been / will be stored about you. <br />
							In order to ensure any information collected by this web application is removed, please <strong>exit</strong> your 
							web browser. (Do not just close this tab)</p>
							
							<div class="clear"></div>
						</form>
					</div>
				</div>
			</div>
		</div>
	</body>
</html>