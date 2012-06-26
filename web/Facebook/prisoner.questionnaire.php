<?php
	
	// Include any required components.
	include_once("prisoner.classes.php");
	include_once("prisoner.constants.php");
	include_once("prisoner.database.php");
	include_once("prisoner.image.php");
	
	
	/**
	 * Uses PRISONER to get the participant's Facebook information and saves it in a session on our end.
	 * Before requesting any information, this function first checks to make sure that it doesn't already
	 * exist in the session. This is because calls to get Facebook data through PRISONER can often be expensive
	 * and we don't want to hinder performance.
	 */
	function get_facebook_data($session_cookie) {
		if (!($_SESSION["got_profile_info"])) {
			$profile_info = get_response("/get/Facebook/User/session:Facebook.id", $session_cookie);	# Profile.
			log_msg("Retrieved profile info from Facebook");
			
			// Add JSON data to the session.
			$_SESSION["profile_info"] = $profile_info;
			$_SESSION["got_profile_info"] = true;
		}
		
		if (!($_SESSION["got_friends_list"])) {
			$friends_info = get_response("/get/Facebook/Friends/session:Facebook.id", $session_cookie);	# Friends.
			log_msg("Retrieved friends list from Facebook");
			
			// Add JSON data to the session.
			$_SESSION["friends_list"] = $friends_info["_objects"];
			$_SESSION["got_friends_list"] = true;
		}
		
		if (!($_SESSION["got_likes_info"])) {
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
			$_SESSION["got_likes_info"] = true;
		}
		
		if (!($_SESSION["got_checkin_info"])) {
			$checkin_info = get_response("/get/Facebook/Checkin/session:Facebook.id", $session_cookie);	# Check-ins.
			log_msg("Retrieved check-in info from Facebook");
			
			// Add JSON data to the session.
			$_SESSION["checkin_info"] = $checkin_info["_objects"];
			$_SESSION["got_checkin_info"] = true;
		}
		
		if (!($_SESSION["got_status_update_info"])) {
			$status_update_info = get_response("/get/Facebook/Status/session:Facebook.id", $session_cookie);	# Status updates.
			log_msg("Retrieved status update info from Facebook");
			
			// Add JSON data to the session.
			$_SESSION["status_update_info"] = $status_update_info["_objects"];
			$_SESSION["got_status_update_info"] = true;
		}
		
		if (!($_SESSION["got_photo_album_info"])) {
			$photo_album_info = get_response("/get/Facebook/Album/session:Facebook.id", $session_cookie);	# Photo album.
			log_msg("Retrieved photo album info from Facebook");
				
			// Add JSON data to the session.
			$_SESSION["photo_album_info"] = $photo_album_info["_objects"];
			$_SESSION["got_photo_album_info"] = true;
		}
		
		if (!($_SESSION["got_photo_info"])) {
			$photo_info = get_response("/get/Facebook/Photo/session:Facebook.id", $session_cookie);	# Photos of.
			log_msg("Retrieved photo info from Facebook");
		
			// Add JSON data to the session.
			$_SESSION["photo_info"] = $photo_info["_objects"];
			$_SESSION["got_photo_info"] = true;
		}
	}
	
	function load_profile_info($session_cookie) {
		if (!($_SESSION["got_profile_info"])) {
			$profile_info = get_response("/get/Facebook/User/session:Facebook.id", $session_cookie);
			log_msg("Retrieved profile info from Facebook");
				
			// Add JSON data to the session.
			$_SESSION["profile_info"] = $profile_info;
			$_SESSION["got_profile_info"] = true;
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
		
		// If we haven't already counted the question types...
		if (!$_SESSION["counted_question_types"]) {
			// Create objects to hold info about question numbers.
			$profile_info_obj = new InfoType("Profile", TYPE_PROFILE);
			$friends_info_obj = new InfoType("Friends", TYPE_FRIEND);
			$likes_info_obj = new InfoType("Likes", TYPE_LIKE);
			$checkins_info_obj = new InfoType("Check-ins", TYPE_CHECKIN);
			$statuses_info_obj = new InfoType("Statuses", TYPE_STATUS);
			$albums_info_obj = new InfoType("Albums", TYPE_ALBUM);
			$photos_info_obj = new InfoType("Photos", TYPE_PHOTO);
			
			// Retrieve the guideline amounts for each item.
			$num_questions = NUM_QUESIONS;
			$profile_info_obj->num_want = NUM_PROFILE_QUESIONS;
			$friends_info_obj->num_want = NUM_FRIENDS_QUESIONS;
			$likes_info_obj->num_want = NUM_LIKES_QUESIONS;
			$checkins_info_obj->num_want = NUM_CHECKIN_QUESIONS;
			$statuses_info_obj->num_want = NUM_STATUS_QUESIONS;
			$albums_info_obj->num_want = NUM_PHOTO_ALBUM_QUESIONS;
			$photos_info_obj->num_want = NUM_PHOTO_QUESIONS;
			log_msg("Guideline numbers obtained. (Profile: " . $profile_info_obj->num_want . ", Friends: " . $friends_info_obj->num_want .
			", Likes: " . $likes_info_obj->num_want .  ", Check-ins " . $checkins_info_obj->num_want . ", Statuses: " . $statuses_info_obj->num_want .
			", Albums: " . $albums_info_obj->num_want . ", Photos: " . $photos_info_obj->num_want . ")");
			
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
			
			// How many photo albums do we have?
			$albums_info_obj->num_have = count($_SESSION["photo_album_info"]);
			log_msg("Participant has " . $albums_info_obj->num_have . " photo albums available.");
			
			// How many photos do we have?
			$photos_info_obj->num_have = count($_SESSION["photo_info"]);
			log_msg("Participant has " . $photos_info_obj->num_have . " photos available.");
			
			// How much info do we have in total?
			$num_infos = $profile_info_obj->num_have + $friends_info_obj->num_have + $likes_info_obj->num_have + $checkins_info_obj->num_have
			+ $statuses_info_obj->num_have + $albums_info_obj->num_have;
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
				$albums_info_obj = get_extra_needed($albums_info_obj);
				$photos_info_obj = get_extra_needed($photos_info_obj);
					
				// Add our info objects into an array we can iterate over.
				$info_array = array();
				$info_array[] = $profile_info_obj;
				$info_array[] = $friends_info_obj;
				$info_array[] = $likes_info_obj;
				$info_array[] = $checkins_info_obj;
				$info_array[] = $statuses_info_obj;
				$info_array[] = $albums_info_obj;
				$info_array[] = $photos_info_obj;
					
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
					
				$_SESSION["counted_question_types"] = true;
				return $info_array;
			}
		}
		
		// If we've already done this, just return true.
		else {
			return true;
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
		// Globals.
		global $PROFILE_INFO_KEYS;
		
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
		
		// What are we going to show to the user? (Profile info is a special case)
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
		$profile_info_keys = $PROFILE_INFO_KEYS;
		$questions[] = get_profile_question($profile_info, "_gender");	# Required.
		$num_profile_questions -= 1;
		unset($profile_info_keys[array_search("_gender", $profile_info_keys)]);
		$questions[] = get_profile_question($profile_info, "_updatedTime");	# Required.
		$num_profile_questions -= 1;
		unset($profile_info_keys[array_search("_updatedTime", $profile_info_keys)]);
		$questions[] = get_profile_question($profile_info, "_image");	# Required.
		$num_profile_questions -= 1;
		unset($profile_info_keys[array_search("_image", $profile_info_keys)]);
		$questions[] = get_profile_question($profile_info, "_hometown");	# Required.
		$num_profile_questions -= 1;
		unset($profile_info_keys[array_search("_hometown", $profile_info_keys)]);
		$questions[] = get_profile_question($profile_info, "_education");	# Required.
		$num_profile_questions -= 1;
		unset($profile_info_keys[array_search("_education", $profile_info_keys)]);
		$questions[] = get_profile_question($profile_info, "_work");	# Required.
		$num_profile_questions -= 1;
		unset($profile_info_keys[array_search("_work", $profile_info_keys)]);
		
		// Now we've got the required info, select the keys we'll ask questions for.
		$profile_questions = array_rand($profile_info_keys, $num_profile_questions);
		
		foreach ($profile_questions as $key) {
			$key = $profile_info_keys[$key];
			log_msg("- Profile info: Getting question for key " . $key);
			$questions[] = get_profile_question($profile_info, $key);
		}
		
		// Questions about the participant's friends.
		foreach ($friend_questions as $key) {
			// Get info about this friend.
			$friend_name = $friends[$key]["_displayName"];
			$friend_pic = $friends[$key]["_image"]["_fullImage"];
			
			// Create question object and add it to our list.
			$this_question = new Question(TYPE_FRIEND, $friend_name);
			$this_question->image = $friend_pic;
			$questions[] = $this_question;
		}
		
		// Questions about the pariticpant's interests.
		foreach ($like_questions as $key) {
			// Get info about this interest.
			$like_name = $likes[$key]["_displayName"];
			
			// Create question object and add it to our list.
			$this_question = new Question(TYPE_LIKE, $like_name);
			$questions[] = $this_question;
		}
		
		// Questions about places the participant has been.
		foreach ($checkin_questions as $key) {
			// Get info about this check-in.
			$place_name = $checkins[$key]["_location"]["_displayName"];
			$time = $checkins[$key]["_published"];
			$timestamp = parse_prisoner_time($time);
			
			// Create question object and add it to our list.
			$this_question = new Question(TYPE_CHECKIN, $place_name);
			$this_question->timestamp = $timestamp;
			$questions[] = $this_question;
		}
		
		// Questions about the pariticpant's status updates.
		foreach ($status_questions as $key) {
			// Get info about the status update.
			$update_text = $status_updates[$key]["_content"];
			$privacy = $status_updates[$key]["_privacy"];
			$time = $status_updates[$key]["_published"];
			$timestamp = parse_prisoner_time($time);
			
			// Create question object and add it to our list.
			$this_question = new Question(TYPE_STATUS, $update_text);
			$this_question->timestamp = $timestamp;
			$this_question->privacy_of_data = $privacy;
			$questions[] = $this_question;
		}
		
		// Questions about the participant's photo albums.
		foreach ($photo_album_questions as $key) {
			// Get info about the album.
			$album_name = $photo_albums[$key]["_displayName"];
			$privacy = $photo_albums[$key]["_privacy"];
			$time = $photo_albums[$key]["_published"];
			$timestamp = parse_prisoner_time($time);
			$extra_info = array();
			$extra_info["num_photos"] = $photo_albums[$key]["_count"];
				
			// Create question object and add it to our list.
			$this_question = new Question(TYPE_ALBUM, $album_name);
			$this_question->timestamp = $timestamp;
			$this_question->privacy_of_data = $privacy;
			$this_question->additional_info = $extra_info;
			$questions[] = $this_question;
		}
		
		// Questions about the pariticpant's photos.
		foreach ($photo_questions as $key) {
			// Get info about the album.
			$photo_name = $photos[$key]["_displayName"];
			$photo = $photos[$key]["_image"]["_fullImage"];
			$time = $photos[$key]["_published"];
			$timestamp = parse_prisoner_time($time);
			$extra_info = array();
			
			// Create question object and add it to our list.
			$this_question = new Question(TYPE_PHOTO, $photo_name);
			$this_question->timestamp = $timestamp;
			$this_question->image = $photo;
			$this_question->additional_info = $extra_info;
			$questions[] = $this_question;
		}
		
		// Randomise array and return.
		log_msg("- Generated " . count($questions) . " questions for the participant.");
		shuffle($questions);
		return $questions;
	}
	
	
	/**
	 * Given a valid key, this function will return a question object for that piece of information.
	 * This function is necessary because, unlike data such as photo albums and status updates, profile information
	 * has a certain amount of context. For example, we cannot use generic phrases for the questions.
	 * This function therefore creates questions that have appropriate preambles and so on.
	 * @param array $profile_info Array of profile information.
	 * @param string $data_key Key to generate question for.
	 */
	function get_profile_question($profile_info, $data_key) {
		switch ($data_key) {
			// Username.
			case "_username":
				return get_profile_question_obj($profile_info, $data_key, "Your Facebook username is");
				break;
			
			// Display name.
			case "_displayName":
				return get_profile_question_obj($profile_info, $data_key, "Your Facebook display name is");
				break;
			
			// First name.
			case "_firstName":
				return get_profile_question_obj($profile_info, $data_key, "Your first name is");
				break;
				
			// Middle name.
			case "_middleName":
				$this_question = get_profile_question_obj($profile_info, $data_key, "Your middle name is");
				
				if (!$this_question) {
					$this_question = new Question(TYPE_PROFILE, "");
					$this_question->custom_question_text = "You either do not have a middle name or have not added it to Facebook";
				}
				
				return $this_question;
				break;
			
			// Last name.
			case "_lastName":
				return get_profile_question_obj($profile_info, $data_key, "Your last name is");
				break;
			
			// Birthday.
			case "_birthday":
				$this_question = get_profile_question_obj($profile_info, $data_key, "Your birthday is");
				
				// No info.
				if (!$this_question) {
					$this_question = new Question(TYPE_PROFILE, "");
					$this_question->custom_question_text = "You have not added your date of birth to Facebook";
				}
				
				// If birthday info exists, remember to format it correctly.
				else {
					$birthday_timestamp = parse_prisoner_time($this_question->text_data);
					$birthday = date("d/m/Y", $birthday_timestamp);
					$this_question->text_data = $birthday;
				}
				
				return $this_question;
				break;
			
			// Gender.
			case "_gender":
				return get_profile_question_obj($profile_info, $data_key, "You are");
				break;
			
			// Bio.
			case "_bio":
				$this_question = get_profile_question_obj($profile_info, $data_key, "Your Facebook bio / about section is");
				
				if (!$this_question) {
					$this_question = new Question(TYPE_PROFILE, "");
					$this_question->custom_question_text = "You have not added a bio / about section to Facebook";
				}
				
				return $this_question;
				break;
			
			// Political views.
			case "_politicalViews":
				$this_question = get_profile_question_obj($profile_info, $data_key, "Your political alignment is");
				
				if (!$this_question) {
					$this_question = new Question(TYPE_PROFILE, "");
					$this_question->custom_question_text = "You have not added information about your political alignment to Facebook";
				}
				
				return $this_question;
				break;
			
			// Religious views.
			case "_religion":
				$this_question = get_profile_question_obj($profile_info, $data_key, "You are");
				
				if (!$this_question) {
					$this_question = new Question(TYPE_PROFILE, "");
					$this_question->custom_question_text = "You have not added information about your religion to Facebook";
				}
				
				return $this_question;
				break;
			
			// Relationship status.
			case "_relationshipStatus":
				$this_question = get_profile_question_obj($profile_info, $data_key, "You are");
				
			if (!$this_question) {
				$this_question = new Question(TYPE_PROFILE, "");
				$this_question->custom_question_text = "Information about your relationship status is not available.";
			}
				
			return $this_question;
			break;
		
			// Interested in.
			case "_interestedIn":
				$this_question = get_profile_question_obj($profile_info, $data_key, "You are interested in");
			
				if (!$this_question) {
					$this_question = new Question(TYPE_PROFILE, "");
					$this_question->custom_question_text = "Information about your sexual orientation is not available.";
				}
				
				else {
					$friendly_list = get_friendly_list($this_question->text_data, true);
					$this_question->text_data = $friendly_list;
				}
			
				return $this_question;
				break;
			
			// Languages.
			case "_languages":
				$this_question = get_profile_question_obj($profile_info, $data_key, "You know");
						
				if (!$this_question) {
					$this_question = new Question(TYPE_PROFILE, "");
					$this_question->custom_question_text = "Information about the languages you know is not available.";
				}
				
				else {
					$friendly_list = get_friendly_list($this_question->text_data, true);
					$this_question->text_data = $friendly_list;
				}
						
				return $this_question;
				break;
			
			// Timezone.
			case "_timezone":
				return get_profile_question_obj($profile_info, $data_key, "Your timezone is");
				break;
			
			// Email address.
			case "_email":
				return get_profile_question_obj($profile_info, $data_key, "Your email address is");
				break;
			
			// Last Facebook update.
			case "_updatedTime":
				$last_update = parse_prisoner_time($profile_info[$data_key]);
				$last_update = date("d/m/Y @ H:i:s", $last_update);
				$this_question = new Question(TYPE_PROFILE, $last_update);
				$this_question->custom_question_text = "You last updated your Facebook profile (From Facebook itself, not via an app) on";
				return $this_question;
				break;
			
			// Profile picture.
			case "_image":
				$profile_pic = $profile_info[$data_key]["_fullImage"];
				$profile_pic = "<img alt='Profile Picture' src='" . $profile_pic . "' />";
				$this_question = new Question(TYPE_PROFILE, $profile_pic);
				$this_question->custom_question_text = "Your current profile picture can be seen on the right";
				return $this_question;
				break;
			
			// Hometown.
			case "_hometown":
				$hometown = $profile_info[$data_key];
				
				// If hometown information is available.
				if (assert_has_name($hometown)) {
					$place_name = $hometown["_displayName"];
					$this_question = new Question(TYPE_PROFILE, $place_name);
					$this_question->custom_question_text = "You are from";
					return $this_question;
				}
				
				// No info available.
				else {
					$this_question = new Question(TYPE_PROFILE, "");
					$this_question->custom_question_text = "You have not added information about your hometown to Facebook.";
					return $this_question;
				}
				
				break;
			
			// Current location.
			case "_location":
				$location = $profile_info[$data_key];
				
				// If location information is available.
				if (assert_has_name($location)) {
					$place_name = $location["_displayName"];
					$this_question = new Question(TYPE_PROFILE, $place_name);
					$this_question->custom_question_text = "You are currently at";
					return $this_question;
				}
				
				// No info available.
				else {
					$this_question = new Question(TYPE_PROFILE, "");
					$this_question->custom_question_text = "You have not added information about your current location to Facebook";
					return $this_question;
				}
				
				break;
				
			// Significant other.
			case "_significantOther":
				$significant_other = $profile_info[$data_key];
				
				// If location information is available.
				if (assert_has_name($significant_other)) {
					$name = $significant_other["_displayName"];
					$this_question = new Question(TYPE_PROFILE, $name);
					$this_question->custom_question_text = "Your significant other is";
					return $this_question;
				}
				
				// No info available.
				else {
					$this_question = new Question(TYPE_PROFILE, "");
					$this_question->custom_question_text = "Information about your significant other is not available on Facebook";
					return $this_question;
				}
				
				break;
			
			// Education history.
			case "_education":
				$education_history = $profile_info[$data_key];
				
				// If the user has education history available.
				if (assert_has_objects($education_history)) {
					$education_history = $education_history["_objects"];
					$place_list = get_friendly_list($education_history);
					
					// Create and return question object.
					$this_question = new Question(TYPE_PROFILE, $place_list);
					$this_question->custom_question_text = "Your education history includes places such as";
					return $this_question;
				}
				
				// No info available.
				else {
					$this_question = new Question(TYPE_PROFILE, "");
					$this_question->custom_question_text = "You have not added information about your education history to Facebook";
					return $this_question;
				}
				
				break;
				
				// Employment history.
				case "_work":
					$work_history = $profile_info[$data_key];
				
					// If the user has work history available.
					if (assert_has_objects($work_history)) {
						$work_history = $work_history["_objects"];
						$place_list = get_friendly_list($work_history);
						
						// Create and return question object.
						$this_question = new Question(TYPE_PROFILE, $place_list);
						$this_question->custom_question_text = "You have worked for employers such as";
						return $this_question;
					}
				
					// No info available.
					else {
						$this_question = new Question(TYPE_PROFILE, "");
						$this_question->custom_question_text = "You have not added information about your work history to Facebook";
						return $this_question;
					}
				
					break;
		}
	}
	
	
	/**
	 * Simple function to generate a question object for a piece of profile information. This function exists because
	 * profile and personal information often has context and so we can't simply use generic question text. (Eg: You live in St Andrews, 
	 * You were born on 01/01/1970)
	 * This function will only work for simple types where the data key directly accesses a piece of text.
	 * @param array $profile_info Array of profile information.
	 * @param string $data_key Key to access.
	 * @param string $question_text Custom text for this question.
	 * @return Question A Question object.
	 */
	function get_profile_question_obj($profile_info, $data_key, $question_text) {
		// Get the value associated with the supplied key.
		$data_value = $profile_info[$data_key];
		
		// No data exists.
		if (empty($data_value)) {
			return false;
		}
		
		// Data exists.
		else {
			// Create and return question object.
			$this_question = new Question(TYPE_PROFILE, $data_value);
			$this_question->custom_question_text = $question_text;
			
			return $this_question;
		}
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
		log_msg("No questions of type " . $question_type . " found.");
		return 0;
	}
	
	
	/**
	 * Returns the HTML markup that should be used to display the supplied question.
	 * Takes a Question object as a parameter.
	 * @param Question $question The question to generate markup for.
	 * @return string A string representation of the markup that should be used to display this question.
	 */
	function get_question_markup($question, $question_number) {
		// Get question info.
		$type = $question->type;
		$text_data = $question->text_data;
		$response = $question->response;
		
		// Generate markup.
		$markup = "<div class='statement'>";
		$markup .= "<div class='statement_info'><p>Question #" . $question_number . ", Category: " . get_friendly_type($type) . "</p></div>" . "\n";
		
		switch ($type) {
			case TYPE_PROFILE:
				$data_item = $question->text_data;
				$question_text = $question->custom_question_text;
				$markup .= "<p>" . $question_text . " <strong>" . $data_item . "</strong>.</p>";
				break;
			
			case TYPE_FRIEND:
				$friend_pic = $question->image;
				$markup .= "<p>You are friends with <strong>" . $text_data . "</strong>.</p>";
				break;
			
			case TYPE_LIKE:
				$markup .= "<p>You like <strong>" . $text_data . "</strong>.</p>";
				break;
			
			case TYPE_CHECKIN:
				$date = date("l j F Y", $question->timestamp);
				$markup .= "<p>You were tagged at <strong>" . $text_data . "</strong> on <strong>" . $date . "</strong>.</p>";
				break;
			
			case TYPE_STATUS:
				$date = date("l j F Y", $question->timestamp);
				$time = date("H:i", $question->timestamp);
				$markup .= "<p>You posted saying <em>&quot;" . $text_data . "&quot;</em> on <strong>" . $date . "</strong> at <strong>" .
				$time . "</strong>.</p>";
				break;
			
			case TYPE_ALBUM:
				$date = date("l j F Y", $question->timestamp);
				$num_photos = $question->additional_info["num_photos"];
				$markup .= "<p>You added photos to an album called <strong>" . $text_data . "</strong> on <strong>" . $date . "</strong>. " .
				"There are <strong>" . $num_photos . "</strong> photos in the album.</p>";
				break;
			
			case TYPE_PHOTO:
				$date = date("l j F Y", $question->timestamp);
				$filename = rand() . ".jpg";
				$image_address = $question->image;
				$image_info = getimagesize($image_address);
				$image_width = $image_info["width"];
				$image_height = $image_info["height"];
				$landscape = true;
				
				if ($image_height > $image_width) {
					$landscape = false;
				}
				
				$image_adjuster = new resize($image_address);
				$image_adjuster->resizeImage(500, 500);
				$image_adjuster->saveImage($filename, 100);
				
				$markup .= "<p>A photo you are tagged in can be seen below.</p>";
				$markup .= "<img alt='Facebook Photo' src='" . $filename . "' />";
				break;
		}
		
		$markup .= "</div>";
		return $markup;
	}
	
	
	/**
	 * Returns a friendly string representation of a question's type. Helpful for clarifying what is being
	 * asked of a user.
	 * @param int $type_id A valid type ID.
	 * @return string A friendly name for the supplied type ID.
	 */
	function get_friendly_type($type_id) {
		switch ($type_id) {
			case TYPE_PROFILE:
				return "Profile and personal information";
				break;
			
			case TYPE_FRIEND:
				return "Friends and acquaintances";
				break;
			
			case TYPE_LIKE:
				return "Likes and interests";
				break;
			
			case TYPE_CHECKIN:
				return "Check-ins and places you've been";
				break;
			
			case TYPE_STATUS:
				return "Status updates";
				break;
			
			case TYPE_ALBUM:
				return "Photos and photo albums";
				break;
				
			case TYPE_PHOTO:
				return "Photos and photo albums";
				break;
				
			default:
				return "General";
		}
	}
	
	
	/**
	 * Returns a user-friendly comma-separated list for collection items.
	 * The display name for each object will be used to represent it in the list.
	 * @param array collection An array of objects.
	 * @return string A comma-separated list that can be used to displau info to users.
	 */
	function get_friendly_list($collection, $is_array = false) {
		$num_items = count($collection);
		$friendly_list = "";
		
		for ($i = 0; $i < $num_items; $i ++) {
			if (!$is_array) {
				$friendly_list .= ucwords($collection[$i]["_displayName"]);
			}
			
			else {
				$friendly_list .= ucwords($collection[$i]);
			}
			
			if ($num_items > 1) {
				if ($i == ($num_items - 2)) {
					$friendly_list .= " and ";
				}
					
				else if ($i < ($num_items - 1)) {
					$friendly_list .= ", ";
				}
			}
		}
		
		return $friendly_list;
	}
	
	
	/**
	 * Parses a date / time object returned by PRISONER and returns a timestamp.
	 * @param array $time_obj
	 * @return number
	 */
	function parse_prisoner_time($time_obj) {
		$time_obj = str_replace("datetime/datetime.datetime(", "", $time_obj["py/repr"]);
		$time_obj = str_replace(")", "", $time_obj);
		
		// Indices will be of the following order: YYYY MM DD HH II SS
		$time_array = explode(", ", $time_obj);
		
		// Seconds seem to disappear if they're exactly 00. This breaks strtotime(), so add seconds in.
		if (!$time_array[5]) {
			$time_array[5] = 00;
		}
		
		// Compose a string and parse it.
		$time_str = $time_array[0] . "-" . $time_array[1] . "-" . $time_array[2] . " " . $time_array[3] . ":" . $time_array[4] . ":" . $time_array[5];
		$timestamp = strtotime($time_str);
		
		return $timestamp;
	}
	
?>