<?php

	// Include any required components.
	include_once("prisoner.constants.php");
	include_once("prisoner.core.php");
	
	// Database config.
	$db_host = DATABASE_HOST;
	$db_user = DATABASE_USER;
	$db_pass = DATABASE_PASS;
	$db_name = "facebook_study";
	
	// Group counters.
	$num_questions = 0;
	$num_shares = 0;
	$num_group_1_questions = 0;
	$num_group_2_questions = 0;
	$num_group_1_yes = 0;
	$num_group_2_yes = 0;
		
	// Question counters.
	$num_profile_questions = 0;
	$num_friend_questions = 0;
	$num_like_questions = 0;
	$num_checkin_questions = 0;
	$num_status_questions = 0;
	$num_album_questions = 0;
	$num_photo_questions = 0;
	$num_profile_yes = 0;
	$num_friend_yes = 0;
	$num_like_yes = 0;
	$num_checkin_yes = 0;
	$num_status_yes = 0;
	$num_album_yes = 0;
	$num_photo_yes = 0;
	
	// Privacy counters.
	$num_everyone = 0;
	$num_friends = 0;
	$num_friends_of = 0;
	$num_custom = 0;
	$num_everyone_yes = 0;
	$num_friends_yes = 0;
	$num_friends_of_yes = 0;
	$num_custom_yes = 0;
	
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
		echo '"Participant ID"' . "\t" . '"Group ID"' . "\t" . '"Info Type ID"' . "\t" . '"Info Type"' . "\t" . '"Privacy Setting"' . "\t" . '"Response"' . "\n";
		$row_count = 0;
		
		while ($row = mysqli_fetch_array($result)) {
			$participant_id = $row["participant_id"];
			$group_id = $row["group_id"];
			$info_type = $row["info_type"];
			$privacy = $row["privacy"];
			$response = $row["response"];
			
			if ($response != 1) {
				$response = 0;
			}
			
			increment_questions($response);
			increment_group($group_id);
			increment_response($group_id, $info_type, $response);
			$row_count ++;			
			
			echo $participant_id . "\t" . $group_id . "\t" . $info_type . "\t" . '"' . get_info_type($info_type) . '"' . "\t" . '"' . $privacy . '"' . "\t" . $response . "\n";
		}
	}
	
	echo "<br/><br/><br/>";
	echo "Total questions: " . $num_questions . "<br />";
	echo "Total shares: " . $num_shares . " (" . round((($num_shares / $num_questions) * 100), 2) . "%)<br />";
	echo "Total group 1: " . $num_group_1_questions . "<br />";
	echo "Total group 2: " . $num_group_2_questions . "<br />";
	echo "Group 1 Shares: " . $num_group_1_yes . " (" . round((($num_group_1_yes / $num_group_1_questions) * 100), 2) . "%)<br />";
	echo "Group 2 Shares: " . $num_group_2_yes . " (" .  round((($num_group_2_yes / $num_group_2_questions) * 100), 2) . "%<br />";
	echo "<br />";
	echo "Total profile info: " . $num_profile_questions . "<br />";
	echo "Total friend info: " . $num_friend_questions . "<br />";
	echo "Total like / interest info: " . $num_like_questions . "<br />";
	echo "Total check-in info: " . $num_checkin_questions . "<br />";
	echo "Total status info: " . $num_status_questions . "<br />";
	echo "Total photo album info: " . $num_album_questions . "<br />";
	echo "Total photo info: " . $num_photo_questions . "<br />";
	echo "Total profile info shares: " . $num_profile_yes . " (" . round((($num_profile_yes / $num_profile_questions) * 100), 2) . "%)<br />";
	echo "Total friend info shares: " . $num_friend_yes . " (" . round((($num_friend_yes / $num_friend_questions) * 100), 2) . "%)<br />";
	echo "Total like / interest info shares: " . $num_like_yes . " (" . round((($num_like_yes / $num_like_questions) * 100), 2) . "%)<br />";
	echo "Total check-in info shares: " . $num_checkin_yes . " (" . round((($num_checkin_yes / $num_checkin_questions) * 100), 2) . "%)<br />";
	echo "Total status info shares: " . $num_status_yes . " (" . round((($num_status_yes / $num_status_questions) * 100), 2) . "%)<br />";
	echo "Total photo album info shares: " . $num_album_yes . " (" . round((($num_album_yes / $num_album_questions) * 100), 2) . "%)<br />";
	echo "Total photo info shares: " . $num_photo_yes . " (" . round((($num_photo_yes / $num_photo_questions) * 100), 2) . "%)<br />";
	echo "<br />";
	echo "";
	
	
	function reduce_privacy($privacy) {
		switch ($privacy) {
			case "N/A":
				return "N/A";
				break;
			
			case "FRIENDS":
				return "FRIENDS";
				break;
			
			case "FRIENDS-OF-FRIENDS":
				return "FRIENDS-OF-FRIENDS";
				break;
			
			case "EVERYONE":
				return "EVERYONE";
				break;
			
			default:
				return "CUSTOM";
				break;
		}
	}
	
	function get_info_type($info_type_id) {
		switch ($info_type_id) {
			case TYPE_PROFILE:
				return "Profile Info";
				break;
			
			case TYPE_FRIEND:
				return "Friend";
				break;
			
			case TYPE_LIKE:
				return "Like / Interest";
				break;
			
			case TYPE_CHECKIN:
				return "Check-in";
				break;
			
			case TYPE_STATUS:
				return "Status Update";
				break;
			
			case TYPE_ALBUM:
				return "Photo Album";
				break;
			
			case TYPE_PHOTO:
				return "Photo";
				break;
		}
	}
	
	
	function increment_group($group_id) {
		global $num_group_1_questions, $num_group_2_questions;
		
		switch ($group_id) {
			case 1:
				$num_group_1_questions ++;
				break;
			
			case 2:
				$num_group_2_questions ++;
				break;
		}
	}
	
	
	function increment_privacy_responses($privacy, $response) {
		global $num_everyone, $num_friends, $num_friends_of, $num_custom, $num_everyone_yes, $num_friends_yes, $num_friends_of_yes, $num_custom_yes;
		
		switch ($privacy) {
			case "N/A":
				break;
			
			case "FRIENDS":
				$num_friends ++;
				break;
			
			case "FRIENDS-OF-FRIENDS":
				$num_friends_of ++;
				break;
			
			case "EVERYONE":
				$num_everyone ++;
				break;
			
			default:
				$num_custom ++;
				break;
		}
		
		if ($response) {
			switch ($privacy) {
				case "N/A":
					break;
				
				case "FRIENDS":
					$num_friends_yes ++;
					break;
				
				case "FRIENDS-OF-FRIENDS":
					$num_friends_of_yes ++;
					break;
				
				case "EVERYONE":
					$num_everyone_yes ++;
					break;
				
				default:
					$num_custom_yes ++;
					break;
			}
		}
	}
	
	
	function increment_response($group_id, $question_type, $response) {
		global $num_group_1_questions, $num_group_2_questions, $num_group_1_yes, $num_group_2_yes, $num_profile_questions, $num_friend_questions, $num_like_questions, $num_checkin_questions,
		$num_status_questions, $num_album_questions, $num_photo_questions, $num_profile_yes, $num_friend_yes, $num_like_yes, $num_checkin_yes, $num_status_yes, $num_album_yes, $num_photo_yes;
		
		switch ($question_type) {
			case TYPE_PROFILE:
				$num_profile_questions ++;
				break;
			
			case TYPE_FRIEND:
				$num_friend_questions ++;
				break;
			
			case TYPE_LIKE:
				$num_like_questions ++;
				break;
			
			case TYPE_CHECKIN:
				$num_checkin_questions ++;
				break;
			
			case TYPE_STATUS:
				$num_status_questions ++;
				break;
			
			case TYPE_ALBUM:
				$num_album_questions ++;
				break;
			
			case TYPE_PHOTO:
				$num_photo_questions ++;
				break;
		}
		
		if ($response) {
			switch ($group_id) {
				case 1:
					$num_group_1_yes ++;
					break;
				
				case 2:
					$num_group_2_yes ++;
					break;
			}
			
			switch ($question_type) {
				case TYPE_PROFILE:
				$num_profile_yes ++;
				break;
				
				case TYPE_FRIEND:
					$num_friend_yes ++;
					break;
				
				case TYPE_LIKE:
					$num_like_yes ++;
					break;
				
				case TYPE_CHECKIN:
					$num_checkin_yes ++;
					break;
				
				case TYPE_STATUS:
					$num_status_yes ++;
					break;
				
				case TYPE_ALBUM:
					$num_album_yes ++;
					break;
				
				case TYPE_PHOTO:
					$num_photo_yes ++;
					break;
			}
		}
		
	}
	
	
	function increment_questions($response) {
		global $num_questions, $num_shares;
		
		$num_questions ++;
		
		if ($response == 1) {
			$num_shares ++;
		}
	}
	
?>