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
	$book_info = get_response("/get/Facebook/Book/session:Facebook.id", $session_cookie);	# Favourite books.

	$display_name = $profile_info["_displayName"];
	$username = $profile_info["_username"];
	$first_name = $profile_info["_firstName"];
	$last_name = $profile_info["_lastName"];
	$gender = $profile_info["_gender"];
	$email_address = $profile_info["_email"];
	$profile_pic = $profile_info["_image"]["_fullImage"];
	$birthday = $profile_info["_birthday"];
	$last_updated = $profile_info["_updatedTime"];
	$religion = $profile_info["_religion"];
	$bio = $profile_info["_bio"];
	$interested_in = $profile_info["_interestedIn"];
	
	echo "<h1>Hello " . $first_name . " " . $last_name ."</h1>" .
	"<img alt='Facebook Profile Picture' src='" . $profile_pic . "' />" .
	"<p>Here's some of the information we grabbed about you:</p>" .
	"<ul>" .
	"<li>Name: " . $first_name . " " . $last_name . "</li>" .
	"<li>Gender: " . $gender . "</li>" .
	"<li>Birthday: " . $birthday . "</li>" .
	"<li>Email Address: " . $email_address . "</li>" .
	"<li>Religion: " . $religion . "</li>" .
	"<li>Last Updated Facebook: " . $last_updated . "</li>" .
	"<li>Interested In: " . $interested_in[0] . "</li>" .
	"</ul>";
	
	// Get the returned array of friends.
	$friends_array = $friends_info["_objects"];
 	$rand_keys = array_rand($friends_array, 10);
	
 	echo "<p>Some of your friends include:</p><ul>";
 	
 	foreach ($rand_keys as $key) {
 		echo "<li>" . $friends_array[$key]["_displayName"] . "</li>";
 	}
	
 	echo "</ul>";
 	
 	// Get the returned array of music.
 	$music_array = $music_info["_objects"];
 	if (sizeof($music_array) > 0) {
 		$rand_keys = array_rand($music_array, 5);
 		
 		echo "<p>You like:</p><ul>";
 		
 		foreach ($rand_keys as $key) {
 			echo "<li>" . $music_array[$key]["_displayName"] . "</li>";
 		}
 		
 		echo "</ul>";
 	}
 	
 	else {
 		echo "<p>You haven't added your musical preferences to Facebook.</p>";
 	}
 	
 	
 	// Get a random friend's ID.
 	$rand_friend = array_rand($friends_array);
 	$rand_id = $friends_array[$rand_friend]["_id"];
 	echo "<p>Random friend ID: " . $rand_id . "</p>";
 	
 	// Get info for random friend.
 	$profile_info = get_response("/get/Facebook/User/literal:" . $rand_id, $session_cookie);	# Profile.
 	var_dump($profile_info);

?>