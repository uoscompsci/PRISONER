<?php
	
	// Include any required components.
	include_once("prisoner.classes.php");
	include_once("prisoner.constants.php");
	include_once("prisoner.database.php");
	
	
	/**
	 * Uses PRISONER to get the participant's Facebook information and saves it in a session on our end.
	 * Before requesting any information, this function first checks to make sure that it doesn't already
	 * exist in the session. This is because calls to get Facebook data through PRISONER can often be expensive
	 * and we don't want to hinder performance.
	 */
	function get_facebook_data($session_cookie) {
		if (empty($_SESSION["profile_info"])) {
			$profile_info = get_response("/get/Facebook/User/session:Facebook.id", $session_cookie);	# Profile.
			log_msg("Retrieved profile info from Facebook");
			
			// Add JSON data to the session.
			$_SESSION["profile_info"] = $profile_info;
		}
		
		if (empty($_SESSION["friends_list"])) {
			$friends_info = get_response("/get/Facebook/Friends/session:Facebook.id", $session_cookie);	# Friends.
			log_msg("Retrieved friends list from Facebook");
			
			// Add JSON data to the session.
			$_SESSION["friends_list"] = $friends_info["_objects"];
		}
		
		if (empty($_SESSION["likes_info"])) {
			$music_info = get_response("/get/Facebook/Music/session:Facebook.id", $session_cookie);	# Favourite bands.
			log_msg("Retrieved favourite bands from Facebook");
			$movie_info = get_response("/get/Facebook/Movie/session:Facebook.id", $session_cookie);	# Favourite movies.
			log_msg("Retrieved favourite movies from Facebook");
			$book_info = get_response("/get/Facebook/Book/session:Facebook.id", $session_cookie);	# Favourite books.
			log_msg("Retrieved favourite books from Facebook");
			
			// Combine music, movies and books into one object. (Likes)
			$music_array = $music_info["_objects"];
			$movie_array = $movie_info["_objects"];
			$book_array = $book_info["_objects"];
			log_msg("Likes: " . count($music_array) . " bands, " . count($movie_array) . " movies and " . count($book_array) . " books.");
			
			$likes_array = array();
			$likes_array = array_merge($music_array, $movie_array, $book_array);
			log_msg("Combined array has " . count($likes_array) . " items.");
			
			// Add JSON data to the session.
			$_SESSION["likes_info"] = $likes_array;
		}
		
		if (empty($_SESSION["checkin_info"])) {
			$checkin_info = get_response("/get/Facebook/Checkin/session:Facebook.id", $session_cookie);	# Check-ins.
			log_msg("Retrieved check-in info from Facebook");
			
			// Add JSON data to the session.
			$_SESSION["checkin_info"] = $checkin_info["_objects"];
		}
		
		if (empty($_SESSION["status_update_info"])) {
			$status_update_info = get_response("/get/Facebook/Status/session:Facebook.id", $session_cookie);	# Status updates.
			log_msg("Retrieved status update info from Facebook");
			
			// Add JSON data to the session.
			$_SESSION["status_update_info"] = $status_update_info["_objects"];
		}
	}
	
	
	/**
	 * Calculates the number of items from each category of information that should be displayed to the user.
	 * Uses the guideline number for each type as defined in prisoner.constants.php but also adjusts if necessary. (Eg: Not enough check-ins)
	 * If there is not enough information on this profile, the function returns false.
	 * @return An array containing the amount of questions that should be asked for each type of data in the following order -
	 * 1. Profile Info, 2. Friends Info, 3. Likes Info, 4. Check-in Info, 5. Status Update Info.
	 * If there are not enough pieces of information on the participant's Facebook, FALSE is returned.
	 */
	function calculate_num_info_types() {
		// Globals.
		global $PROFILE_INFO_KEYS;
		
		// Create objects to hold info about question numbers.
		$profile_info_obj = new InfoType("Profile", TYPE_PROFILE);
		$friends_info_obj = new InfoType("Friends", TYPE_FRIEND);
		$likes_info_obj = new InfoType("Likes", TYPE_LIKE);
		$checkins_info_obj = new InfoType("Check-ins", TYPE_CHECKIN);
		$statuses_info_obj = new InfoType("Statuses", TYPE_STATUS);
		
		// Retrieve the guideline amounts for each item.
		$num_questions = NUM_QUESIONS;
		$profile_info_obj->num_want = NUM_PROFILE_QUESIONS;
		$friends_info_obj->num_want = NUM_FRIENDS_QUESIONS;
		$likes_info_obj->num_want = NUM_LIKES_QUESIONS;
		$checkins_info_obj->num_want = NUM_CHECKIN_QUESIONS;
		$statuses_info_obj->num_want = NUM_STATUS_QUESIONS;
		log_msg("Guideline numbers obtained. (Profile: " . $profile_info_obj->num_want . ", Friends: " . $friends_info_obj->num_want . 
		", Likes: " . $likes_info_obj->num_want .  ", Check-ins " . $checkins_info_obj->num_want . ", Statuses: " . $statuses_info_obj->num_want . ")");
		
		// How many of each info type do we have?
		$num_infos = 0;
		$num_need_extra = 0;
		
		// How much profile info do we have?
		foreach ($PROFILE_INFO_KEYS as $key) {
			if (!empty($_SESSION["profile_info"][$key])) {
				// Special case for education / work.
				if (($key == "_education") || ($key == "_work")) {
					if (assert_has_objects($_SESSION["profile_info"][$key])) {
						$profile_info_obj->num_have += 1;
					}
				}
				
				// Special case for hometown / location / signigicant other.
				else if (($key == "_hometown") || ($key == "_location") || ($key == "_significantOther")) {
					if (assert_has_name($_SESSION["profile_info"][$key])) {
						$profile_info_obj->num_have += 1;
					}
				}
				
				// General case.
				else {
					$profile_info_obj->num_have += 1;
				}
			}
		}
				
		log_msg("Participant has " . $profile_info_obj->num_have . " pieces of profile info.");
		
		// How much friend info do we have?
		$friends_info_obj->num_have = count($_SESSION["friends_list"]);
		log_msg("Participant has " . $friends_info_obj->num_have . " pieces of friend info.");
		
		// How much likes / interests  info do we have?
		$likes_info_obj->num_have = count($_SESSION["likes_info"]);
		log_msg("Participant has " . $likes_info_obj->num_have . " pieces of likes and interests info.");
		
		// How much check-in info do we have?
		$checkins_info_obj->num_have = count($_SESSION["checkin_info"]);
		log_msg("Participant has " . $checkins_info_obj->num_have . " pieces of check-in info.");
		
		// How much status update info do we have?
		$statuses_info_obj->num_have = count($_SESSION["status_update_info"]);
		log_msg("Participant has " . $statuses_info_obj->num_have . " status updates available.");
		
		// How much info do we have in total?
		$num_infos = $profile_info_obj->num_have + $friends_info_obj->num_have + $likes_info_obj->num_have + $checkins_info_obj->num_have 
		+ $statuses_info_obj->num_have;
		log_msg("Total pieces of info available: " . $num_infos);
		
		// We don't have enough info for the study.
		if ($num_infos < $num_questions) {
			log_msg("Insufficient info available to complete study. (Have " . $num_infos . ", need " . $num_questions . ")");
			return false;
		}
		
		// Otherwise, check we have enough of each type.
		else {
			// Calculate total amount of compensation required.
			$profile_info_obj = get_extra_needed($profile_info_obj);
			$friends_info_obj = get_extra_needed($friends_info_obj);
			$likes_info_obj = get_extra_needed($likes_info_obj);
			$checkins_info_obj = get_extra_needed($checkins_info_obj);
			$statuses_info_obj = get_extra_needed($statuses_info_obj);
			
			// Add our info objects into an array we can iterate over.
			$info_array = array();
			$info_array[] = $profile_info_obj;
			$info_array[] = $friends_info_obj;
			$info_array[] = $likes_info_obj;
			$info_array[] = $checkins_info_obj;
			$info_array[] = $statuses_info_obj;
			
			// Calculate amount of type compensation needed.
			foreach ($info_array as $info_type) {
				if ($info_type->mismatch > 0) {
					$num_need_extra += $info_type->mismatch;
				}
			}
			
			log_msg("Need to compensate for " . $num_need_extra . " pieces of info.");
			
			// We need to compensate for a lack of one or more types of info.
			if ($num_need_extra > 0) {
				$num_category_types = count($info_array);
				$j = 0;
				
				for ($i = 0; $i < $num_need_extra; $i ++) {
					// Hit limit of category types, reset index.
					if ($j == $num_category_types) {
						$j = 0;
					}
					
					// If this info type has spare capacity, use it.
					if ($info_array[$j]->num_spare > 0) {
						$info_array[$j]->num_want += 1;
						$info_array[$j]->num_spare -= 1;
						log_msg("- Assigning extra from " . $info_array[$j]->name . ". (Will ask: " . $info_array[$j]->num_want .
						", New spare capacity: " . $info_array[$j]->num_spare . ")");
					}
					
					$j ++;
				}
			}
			
			return $info_array;
		}
	}
	
	
	/**
	 * Checks the supplied object - a collection type in JSON / array form - has at least 1 item.
	 * @param array $obj The object in associative array format to check.
	 * @return boolean True if the object contains >= 1 item.
	 */
	function assert_has_objects($obj) {
		if (count($obj["_objects"]) >= 1) {
			return true;
		}
		
		else {
			return false;
		}
	}
	
	
	/**
	 * Checks that the supplied object - a Social Object in JSON / array form - has a value for its display name.
	 * Almost all social objects will have a display name, so this function can be used to check to see whether or not 
	 * an object / attribute exists.
	 * @param array $obj
	 * @return boolean True if the object has a display name.
	 */
	function assert_has_name($obj) {
		if (!empty($obj["_displayName"])) {
			return true;
		}
		
		else {
			return false;
		}
	}
	
	
	/**
	 * Calculates the compensation value we'll need to make up later. (If any)
	 * If we have more info than we have questions for a given type, compensation is not required
	 * and so 0 is returned.
	 * @param InfoType $info_obj The info type object to calculate the compensation for.
	 * @return int The amount we'll need to compensate for this piece of info.
	 */
	function get_extra_needed($info_obj) {
		$difference = $info_obj->num_have - $info_obj->num_want;
		$info_obj->num_spare = $difference;
		log_msg("Have " . $info_obj->num_have . ", need " . $info_obj->num_want . ". Difference: " . $difference);
		
		// This item has a mismatch and will require compensating.
		if ($difference < 0) {
			$info_obj->mismatch = ($difference - $difference);
		}
		
		return $info_obj;
	}
	
	
	/**
	 * Generates the questions to ask the participant based on the supplied array that defines the number of
	 * questions per type we need to ask. Returns an array of Question() objects in a random order.
	 * @param array $num_questions_per_type An array of InfoType() objects.
	 * @return An array of Question() objects.
	 */
	function generate_questions($question_info_array) {
		// How many questions of each type do we need?
		$num_profile_questions = get_num_questions_for(TYPE_PROFILE, $question_info_array);
		$num_friends_questions = get_num_questions_for(TYPE_FRIEND, $question_info_array);
		$num_like_questions = get_num_questions_for(TYPE_LIKE, $question_info_array);
		$num_checkin_questions = get_num_questions_for(TYPE_CHECKIN, $question_info_array);
		$num_status_questions = get_num_questions_for(TYPE_STATUS, $question_info_array);
		$num_album_questions = get_num_questions_for(TYPE_ALBUM, $question_info_array);
		$num_photo_questions = get_num_questions_for(TYPE_PHOTO, $question_info_array);
		
		// Get Facebook info from session.
		$profile_info = $_SESSION["profile_info"];
		$friends = $_SESSION["friends_list"];
		$likes = $_SESSION["likes_info"];
		$checkins = $_SESSION["checkin_info"];
		$status_updates = $_SESSION["status_update_info"];
		$photo_albums = $_SESSION["photo_album_info"];
		$photos = $_SESSION["photo_info"];
		
		// What are we going to show to the user?
		$profile_questions = array_rand($profile_info, $num_profile_questions);
		$friend_questions = array_rand($friends, $num_friends_questions);
		$like_questions = array_rand($likes, $num_like_questions);
		$checkin_questions = array_rand($checkins, $num_checkin_questions);
		$status_questions = array_rand($status_updates, $num_status_questions);
		$photo_album_questions = array_rand($photo_albums, $num_album_questions);
		$photo_questions = array_rand($photos, $num_photo_questions);
				
		// Array to hold our questions.
		log_msg("Generating questions to display.");
		$questions = array();
		
		// Questions about the participant's personal profile info.
		foreach ($profile_questions as $key) {
			log_msg("- Profile and personal info: " . $key);
		}
		
		// Questions about the participant's friends.
		foreach ($friend_questions as $key) {
			// Get info about this friend.
			$friend_name = $friends[$key]["_displayName"];
			$friend_pic = $friends[$key]["_image"]["_fullImage"];
			
			// Info to populate question with.
			$question_text = "You are friends with";
			$data_to_display = $friend_name;
			$privacy_of_data = "";
			
			// Create question object and add it to our list.
			$this_question = new Question(TYPE_PROFILE, $question_text, $data_to_display, $privacy_of_data);
			$questions[] = $this_question;
		}
		
		// Questions about the pariticpant's interests.
		foreach ($like_questions as $key) {
			// Get info about this interest.
			$like_name = $likes[$key]["_displayName"];
			
			// Info to populate question with.
			$question_text = "You like";
			$data_to_display = $like_name;
			$privacy_of_data = "";
			
			// Create question object and add it to our list.
			$this_question = new Question(TYPE_PROFILE, $question_text, $data_to_display, $privacy_of_data);
			$questions[] = $this_question;
		}
		
		// Questions about places the participant has been.
		foreach ($checkin_questions as $key) {
			log_msg("- Locations.");
		}
		
		// Questions about the pariticpant's status updates.
		foreach ($status_questions as $key) {
			log_msg("- Status updates.");
		}
		
		// Questions about the pariticpant's photo albums.
		foreach ($photo_album_questions as $key) {
			log_msg("- Photo albums.");
		}
		
		// Questions about the pariticpant's photos.
		foreach ($photo_questions as $key) {
			log_msg("- Photos.");
		}
		
		// Randomise array and return.
		log_msg("- Generated " . count($questions) . " questions for the participant.");
		shuffle($questions);
		return $questions;
	}
	
	
	/**
	 * Loops through the supplied haystack (Probably an array) and returns the number of questions that need to be
	 * asked for the supplied question type.
	 * @param int $question_type Question type to find.
	 * @param array $haystack Array of InfoType() objects.
	 * @return The number of questions to ask of the supplied type. (0 if type not found)
	 */
	function get_num_questions_for($question_type, $haystack) {
		foreach ($haystack as $question) {
			// We've found a match, so return how many questions to ask.
			if ($question->type == $question_type) {
				log_msg("Want " . $question->num_want . " questions of type " . $question->type . ".");
				return $question->num_want;
			}
		}
		
		// No match was found, return 0.
		log_msg("No questions of type " . $question->type . " found.");
		return 0;
	}
	
?>