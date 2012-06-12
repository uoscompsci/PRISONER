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
 	$rand_friend_key = array_rand($friends_array);
 	$rand_friend_id = $friends_array[$rand_friend_key]["_id"];
 	$rand_friend_name = $friends_array[$rand_friend_key]["_displayName"];
 	
 	// Get info for random friend.
 	$rand_friend_info = get_response("/get/Facebook/User/literal:" . $rand_friend_id, $session_cookie);

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
				<h1>PRISONER - Bad Example</h1>
				
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
				<p>We notice you're friends with <strong><?php echo $rand_friend_name; ?></strong> <br />
				Their Facebook username is <strong><?php echo "<" . $rand_friend_info["_username"] . ">"; ?></strong> and their 
				gender is <strong><?php echo "<" . $rand_friend_info["_gender"] . ">"; ?></strong>.</p>
			</div>
		</div>
	</body>
</html>