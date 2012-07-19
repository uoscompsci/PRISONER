<?php

	// Include any required components.
	include_once("prisoner.constants.php");
	include_once("prisoner.core.php");
	
	// Database config.
	$db_host = DATABASE_HOST;
	$db_user = DATABASE_USER;
	$db_pass = DATABASE_PASS;
	$db_name = "facebook_study";
	
	$all_data = array();
	$participant_ids = array();
	
	// Try and connect to the database.
	$db = mysqli_connect($db_host, $db_user, $db_pass, $db_name);
	
	// Connection error.
	if (!$db) {
		echo "Error - Couldn't connect to database server: " . mysqli_error() . "\n";
	}
	
	// All good.
	else {
		$query = "SELECT * FROM response";
		$result = mysqli_query($db, $query);
		
		// Suck all data out of database.
		while ($row = mysqli_fetch_array($result)) {
			$all_data[] = $row;
		}
	}
	
	// Get all participant IDs.
	foreach($all_data as $row) {
		$participant_id = $row["participant_id"];
		
		if (in_array($participant_id, $participant_ids) === false) {
			$participant_ids[] = $participant_id;
		}
	}
	
	foreach($participant_ids as $participant) {
		$results = array();
		$profile_questions = 0;
		$friend_questions = 0;
		$like_questions = 0;
		$checkin_questions = 0;
		$status_questions = 0;
		$album_questions = 0;
		$photo_questions = 0;
		
		$profile_yes = 0;
		$friend_yes = 0;
		$like_yes = 0;
		$checkin_yes = 0;
		$status_yes = 0;
		$album_yes = 0;
		$photo_yes = 0;
		
		$group_id = 0;
		
		foreach($all_data as $row) {
			if ($row["participant_id"] == $participant) {
				$info_type = $row["info_type"];
				$response = $row["response"];
				$group_id =  $row["group_id"];
				
				switch ($info_type) {
					case TYPE_PROFILE:
						$profile_questions ++;
						
						if ($response) {
							$profile_yes ++;
						}
						break;
					
					case TYPE_FRIEND:
						$friend_questions ++;
						if ($response) {
							$friend_yes ++;
						}
						break;
					
					case TYPE_LIKE:
						$like_questions ++;
						if ($response) {
							$like_yes ++;
						}
						break;
					
					case TYPE_CHECKIN:
						$checkin_questions ++;
						if ($response) {
							$checkin_yes ++;
						}
						break;
					
					case TYPE_STATUS:
						$status_questions ++;
						if ($response) {
							$status_yes ++;
						}
						break;
					
					case TYPE_ALBUM:
						$album_questions ++;
						if ($response) {
							$album_yes ++;
						}
						break;
					
					case TYPE_PHOTO:
						$photo_questions ++;
						if ($response) {
							$photo_yes ++;
						}
						break;
				}
			}
		}
		
		echo '"Profile Info"' . "\t" . ($profile_yes / $profile_questions) . "\t" . $group_id . "\n";
		echo '"Friend"' . "\t" . ($profile_yes / $profile_questions) . "\t" . $group_id . "\n";
		echo '"Like / Interest"' . "\t" . ($profile_yes / $profile_questions) . "\t" . $group_id . "\n";
		echo '"Check-in"' . "\t" . ($profile_yes / $profile_questions) . "\t" . $group_id . "\n";
		echo '"Status Update"' . "\t" . ($profile_yes / $profile_questions) . "\t" . $group_id . "\n";
		echo '"Photo Album"' . "\t" . ($profile_yes / $profile_questions) . "\t" . $group_id . "\n";
		echo '"Photo"' . "\t" . ($profile_yes / $profile_questions) . "\t" . $group_id . "\n";
	}
?>