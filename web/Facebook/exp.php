<?php
	
	// Start a session on the server.
	session_start();
	$session_cookie = $_COOKIE["PRISession"];
	
	$ch = curl_init();
	
	// Set options.	
	curl_setopt($ch, CURLOPT_COOKIE, "PRISession=" . $session_cookie);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt($ch, CURLOPT_URL, "http://127.0.0.1:5000/get/Facebook/User/session:Facebook.id");
	
	// Access address and close connection.
	$data = curl_exec($ch);
	curl_close($ch);
	$data = json_decode($data, true);

	$display_name = $data["_displayName"];
	$username = $data["_username"];
	$first_name = $data["_firstName"];
	$last_name = $data["_lastName"];
	$gender = $data["_gender"];
	$email_address = $data["_email"];
	$profile_pic = $data["_image"]["_fullImage"];
	$birthday = $data["_birthday"];
	$last_updated = $data["_updatedTime"];
	$religion = $data["_religion"];
	$bio = $data["_bio"];
	$interested_in = $data["_interestedIn"];
	
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

?>