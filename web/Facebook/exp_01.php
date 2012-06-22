<?php
	
	// Start a session on the server.
	session_start();
	
	// Include any required components.
	include_once("prisoner.authentication.php");
	include_once("prisoner.core.php");

	// Set session.
	set_session();
	$session_cookie = $_SESSION["PRISession_Cookie"];
	
	// Get info from Facebook.
	$profile_info = get_response("/get/Facebook/User/session:Facebook.id", $session_cookie);	# Profile.
	$friends_info = get_response("/get/Facebook/Friends/session:Facebook.id", $session_cookie);	# Friends.
	$music_info = get_response("/get/Facebook/Music/session:Facebook.id", $session_cookie);	# Favourite bands.
	
	// Parse profile information.
	$display_name = $profile_info["_displayName"];
	$username = $profile_info["_username"];
	$first_name = $profile_info["_firstName"];
	$last_name = $profile_info["_lastName"];
	$gender = $profile_info["_gender"];
	$email_address = $profile_info["_email"];
	$profile_pic = $profile_info["_image"]["_fullImage"];
	$hometown = $profile_info["_hometown"];
	$current_location = $profile_info["_location"];
	
	// Check hometown exists.
	if (empty($hometown["_displayName"])) {
		$hometown = "Not available";
	}
	
	else {
		$hometown = $hometown["_displayName"];
	}
	
	// Check current location exists.
	if (empty($current_location["_displayName"])) {
		$current_location = "Not available";
	}
	
	else {
		$current_location = $current_location["_displayName"];
	}
	
	// Parse friend information.
	$friends_array = $friends_info["_objects"];
 	$rand_friend_keys = array_rand($friends_array, 15);
 	
 	// Parse favourite band information.
 	$music_array = $music_info["_objects"];
 	$rand_music_keys = NULL;
 	
 	// Check there's music info available.
 	if (sizeof($music_array) > 0) {
 		$rand_music_keys = array_rand($music_array, 5);
 	}

?>

<!DOCTYPE HTML>
<html>
	<head>
		<?php include_once("prisoner.include.head.php"); ?>
		<title>PRISONER - Hello World Example</title>
	</head>
	
	<body>
		<div class="wrapper">
			<div class="content">
				<img alt="Facebook Profile Picture" src="<?php echo $profile_pic; ?>" />
				<h1>PRISONER - Good Example</h1>
				
				<!--  Profile info. -->
				<p>Hi <?php echo $first_name; ?>. Thanks for taking part in this survey. <br />
				Here's a selection of some of the information we grabbed about you:</p>
				<ul>
					<li>Full name: <?php echo $first_name . " " . $last_name; ?></li>
					<li>Display name: <?php echo $display_name; ?></li>
					<li>Username: <?php echo $username; ?></li>
					<li>Gender: <?php echo $gender; ?></li>
					<li>Email address: <?php echo $email_address; ?></li>
					<li>Hometown: <?php echo $hometown; ?></li>
					<li>Current location: <?php echo $current_location; ?></li>
				</ul>
		
				<!-- Friend info. -->
				<p>Some of your friends include:</p>
				<ul>
					<?php
				
						foreach ($rand_friend_keys as $key) {
							echo "<li>" . $friends_array[$key]["_displayName"] . "</li>" . "\n";
						}
				
					?>
				</ul>
		
				<!-- Music tastes. -->
				<p>Here are some of the bands / musicians you like:</p>
				<ul>
					<?php
				
						// There's music available.
						if ($rand_music_keys) {
							foreach ($rand_music_keys as $key) {
								echo "<li>" . $music_array[$key]["_displayName"] . "</li>" . "\n";
							}
						}
				
						// No info to display.
						else {
							echo "<li>No music preferences available.</li>" . "\n";
						}
					?>
				</ul>
			</div>
		</div>
	</body>
</html>