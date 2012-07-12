<?php

	// Include any required components.
	include_once("prisoner.classes.php");
	include_once("prisoner.constants.php");
	include_once("prisoner.database.php");
	include_once("prisoner.image.php");
	
	
	/**
	 * Loads the initial data that is required from Facebook.
	 * For the experiment to begin, we need to load profile data, friend data and likes / interests data.
	 * This is so we have enough questions to ask whilst larger data objects are being retrieved from PRISONER
	 * such as status updates and photos.
	 * This function is aware of the question_info object in the session and loads data to the correct place.
	 * @param int $session_id
	 */
	function load_init_data($session_id) {
		$question_info = &$_SESSION["question_info"];
		
		// Load profile / personal info if necessary.
		if (!$question_info[TYPE_PROFILE]->loaded_data) {
			$profile_data = get_response("/get/Facebook/User/session:Facebook.id", $session_id);
			$question_info[TYPE_PROFILE]->data = $profile_data;
			$question_info[TYPE_PROFILE]->loaded_data = true;
			log_msg("Retrieved profile / personal info from Facebook.");
		}
		
		else {
			log_msg("Profile / personal info already exists. Ignoring.");
		}
		
		// Load friend data if necessary.
		if (!$question_info[TYPE_FRIEND]->loaded_data) {
			$friend_data = get_response("/get/Facebook/Friends/session:Facebook.id", $session_id);
			$question_info[TYPE_FRIEND]->data = $friend_data["_objects"];
			$question_info[TYPE_FRIEND]->loaded_data = true;
			log_msg("Retrieved friend info from Facebook.");
		}
		
		else {
			log_msg("Friend info already exists. Ignoring.");
		}
		
		// Load likes / interests info if necessary.
		if (!$question_info[TYPE_LIKE]->loaded_data) {
			$music_data = get_response("/get/Facebook/Music/session:Facebook.id", $session_id);
			$movie_data = get_response("/get/Facebook/Movie/session:Facebook.id", $session_id);
			$book_data = get_response("/get/Facebook/Book/session:Facebook.id", $session_id);
			
			$music_array = $music_data["_objects"];
			$movie_array = $movie_data["_objects"];
			$book_array = $book_data["_objects"];
			
			$likes_array = array();
			$likes_array = array_merge($music_array, $movie_array, $book_array);
			
			$question_info[TYPE_LIKE]->data = $likes_array;
			$question_info[TYPE_LIKE]->loaded_data = true;
			log_msg("Retrieved likes / interests info from Facebook.");
		}
		
		else {
			log_msg("Likes / interests info already exists. Ignoring.");
		}
	}
	
	
	/**
	 * Sends async requests for the rest of that data we need from Facebook.
	 * Checks the session before requesting anything so we don't spam PRISONER.
	 */
	function load_additional_data($session_id) {
		// Send async requests to PRISONER for the rest of the data.
		//if (empty($_SESSION["sent_async_requests"])) {
			$checkin_info = get_response("/get/Facebook/Checkin/session:Facebook.id", $session_id, true);	# Check-ins.
			log_msg("Sent async request for check-ins.");
			$status_update_info = get_response("/get/Facebook/Status/session:Facebook.id", $session_id, true);	# Status updates.
			log_msg("Sent async request for status updates.");
			$photo_album_info = get_response("/get/Facebook/Album/session:Facebook.id", $session_id, true);	# Photo album.
			log_msg("Sent async request for photo albums.");
			$photo_info = get_response("/get/Facebook/Photo/session:Facebook.id", $session_id, true);	# Photos of.
			log_msg("Sent async request for photos.");
				
			$_SESSION["sent_async_requests"] = true;
		//}
	}
	
	
	/**
	 * Gets questions of the supplied type.
	 * Uses the supplied question type as a key to get info from the session.
	 * Checks to see how many questions of that type are required and then loops through the necessary
	 * data, generating questions.
	 * Questions are returned as an array of question objects.
	 * @param int $question_type The type of question to get questions for.
	 * @return array An array of question objects. (May be empty)
	 */
	function get_questions($question_type) {
		// Globals.
		global $PROFILE_INFO_KEYS;
		
		log_msg(" - Generating questions.");
		$question_info_obj = &$_SESSION["question_info"][$question_type];
		$question_info_obj->generated_questions = true;
		$questions = array();
		$num_want = &$question_info_obj->num_want;
		$data_items = &$question_info_obj->data;
		$data_keys = NULL;
		
		// If we don't need any questions, return an empty array.
		if ($num_want < 1) {
			log_msg(" - Returned " . count($questions) . " questions.");
			return $questions;
		}
		
		if ($question_type != TYPE_PROFILE) {
			$data_keys = array_rand($data_items, $num_want);
			log_msg(" - Generated " . count($data_keys) . " random data keys to grab.");
		}
		
		switch ($question_type) {
			case TYPE_PROFILE:
				// If we haven't already got these, get the required data items.
				if (empty($_SESSION["got_required_profile_data"])) {
					$questions[] = get_profile_question($data_items, "_gender");	# Required.
					$num_want -= 1;
					unset($PROFILE_INFO_KEYS[array_search("_gender", $PROFILE_INFO_KEYS)]);
					$questions[] = get_profile_question($data_items, "_updatedTime");	# Required.
					$num_want -= 1;
					unset($PROFILE_INFO_KEYS[array_search("_updatedTime", $PROFILE_INFO_KEYS)]);
					$questions[] = get_profile_question($data_items, "_image");	# Required.
					$num_want -= 1;
					unset($PROFILE_INFO_KEYS[array_search("_image", $PROFILE_INFO_KEYS)]);
					$questions[] = get_profile_question($data_items, "_hometown");	# Required.
					$num_want -= 1;
					unset($PROFILE_INFO_KEYS[array_search("_hometown", $PROFILE_INFO_KEYS)]);
					$questions[] = get_profile_question($data_items, "_education");	# Required.
					$num_want -= 1;
					unset($PROFILE_INFO_KEYS[array_search("_education", $PROFILE_INFO_KEYS)]);
					$questions[] = get_profile_question($data_items, "_work");	# Required.
					$num_want -= 1;
					unset($PROFILE_INFO_KEYS[array_search("_work", $PROFILE_INFO_KEYS)]);
					
					$_SESSION["got_required_profile_data"] = true;
				}
				
				// We'll have already got required info, so remove keys for it in case of duplicate questions.
				unset($PROFILE_INFO_KEYS[array_search("_gender", $PROFILE_INFO_KEYS)]);
				unset($PROFILE_INFO_KEYS[array_search("_updatedTime", $PROFILE_INFO_KEYS)]);
				unset($PROFILE_INFO_KEYS[array_search("_image", $PROFILE_INFO_KEYS)]);
				unset($PROFILE_INFO_KEYS[array_search("_hometown", $PROFILE_INFO_KEYS)]);
				unset($PROFILE_INFO_KEYS[array_search("_education", $PROFILE_INFO_KEYS)]);
				unset($PROFILE_INFO_KEYS[array_search("_work", $PROFILE_INFO_KEYS)]);
				
				// Now we've got the required data, select the keys we'll ask questions for.
				$data_keys = array_rand($PROFILE_INFO_KEYS, $num_want);
				
				// Multiple data keys were returned.
				if (is_array($data_keys)) {
					foreach ($data_keys as $key) {
						$key = $PROFILE_INFO_KEYS[$key];
						log_msg("- Profile info: Getting question for key " . $key);
						$questions[] = get_profile_question($data_items, $key);
						$num_want -= 1;
					}
				}
				
				// A single key was returned.
				else {
					$key = $PROFILE_INFO_KEYS[$data_keys];
					log_msg("- Profile info: Getting question for key " . $key);
					$questions[] = get_profile_question($data_items, $key);
					$num_want -= 1;
				}
				
				break;
			
			case TYPE_FRIEND:
				if (is_array($data_keys)) {
					foreach ($data_keys as $key) {
						// Get required info.
						$friend_name = $data_items[$key]["_displayName"];
						$url = $data_items[$key]["_url"];
							
						// Create question object and add it to our list.
						$this_question = new Question(TYPE_FRIEND, $friend_name);
						$this_question->permalink = $url;
						$questions[] = $this_question;
						$num_want -= 1;
					}
					
				}
				
				else {
					// Get required info.
					$friend_name = $data_items[$data_keys]["_displayName"];
						
					// Create question object and add it to our list.
					$this_question = new Question(TYPE_FRIEND, $friend_name);
					$this_question->permalink = $url;
					$questions[] = $this_question;
					$num_want -= 1;
				}
				
				break;
				
			case TYPE_LIKE:
				if (is_array($data_keys)) {
					foreach ($data_keys as $key) {
						// Get required info.
						$like_name = $data_items[$key]["_displayName"];
						$url = $data_items[$key]["_url"];
					
						// Create question object and add it to our list.
						$this_question = new Question(TYPE_LIKE, $like_name);
						$this_question->permalink = $url;
						$questions[] = $this_question;
						$num_want -= 1;
					}
				}
				
				else {
					// Get required info.
					$like_name = $data_items[$data_keys]["_displayName"];
					$url = $data_items[$data_keys]["_url"];
						
					// Create question object and add it to our list.
					$this_question = new Question(TYPE_LIKE, $like_name);
					$this_question->permalink = $url;
					$questions[] = $this_question;
					$num_want -= 1;
				}
				
				break;
					
			case TYPE_CHECKIN:
				if (is_array($data_keys)) {
					foreach ($data_keys as $key) {
						// Get required info.
						$place_name = $data_items[$key]["_location"]["_displayName"];
						$time = $data_items[$key]["_published"];
						$timestamp = parse_prisoner_time($time);
							
						// Create question object and add it to our list.
						$this_question = new Question(TYPE_CHECKIN, $place_name);
						$this_question->timestamp = $timestamp;
						$questions[] = $this_question;
						$num_want -= 1;
					}
				}
				
				else {
					// Get required info.
					$place_name = $data_items[$data_keys]["_location"]["_displayName"];
					$url = $data_items[$data_keys]["_url"];
					$time = $data_items[$data_keys]["_published"];
					$timestamp = parse_prisoner_time($time);
						
					// Create question object and add it to our list.
					$this_question = new Question(TYPE_CHECKIN, $place_name);
					$this_question->timestamp = $timestamp;
					$questions[] = $this_question;
					$num_want -= 1;
				}
				
				break;
						
			case TYPE_STATUS:
				if (is_array($data_keys)) {
					foreach ($data_keys as $key) {
						// Get required info.
						$update_text = $data_items[$key]["_content"];
						$url = $data_items[$key]["_url"];
						$privacy = $data_items[$key]["_privacy"];
						$time = $data_items[$key]["_published"];
						$timestamp = parse_prisoner_time($time);
					
						// Create question object and add it to our list.
						$this_question = new Question(TYPE_STATUS, $update_text);
						$this_question->timestamp = $timestamp;
						$this_question->privacy_of_data = strtoupper($privacy);
						$this_question->permalink = $url;
						$questions[] = $this_question;
						$num_want -= 1;
					}
				}
				
				else {
					// Get required info.
					$update_text = $data_items[$data_keys]["_content"];
					$url = $data_items[$data_keys]["_url"];
					$privacy = $data_items[$data_keys]["_privacy"];
					$time = $data_items[$data_keys]["_published"];
					$timestamp = parse_prisoner_time($time);
						
					// Create question object and add it to our list.
					$this_question = new Question(TYPE_STATUS, $update_text);
					$this_question->timestamp = $timestamp;
					$this_question->privacy_of_data = strtoupper($privacy);
					$this_question->permalink = $url;
					$questions[] = $this_question;
					$num_want -= 1;
				}
				
				break;
							
			case TYPE_ALBUM:
				if (is_array($data_keys)) {
					foreach ($data_keys as $key) {
						// Get required info.
						$album_name = $data_items[$key]["_displayName"];
						$url = $data_items[$key]["_url"];
						$privacy = $data_items[$key]["_privacy"];
						$time = $data_items[$key]["_published"];
						$cover_photo = $data_items[$key]["_coverPhoto"]["_fullImage"];
						$timestamp = parse_prisoner_time($time);
						$extra_info = array();
						$extra_info["num_photos"] = $data_items[$key]["_count"];
							
						// Create question object and add it to our list.
						$this_question = new Question(TYPE_ALBUM, $album_name);
						$this_question->timestamp = $timestamp;
						$this_question->privacy_of_data = strtoupper($privacy);
						$this_question->image = $cover_photo;
						$this_question->permalink = $url;
						$this_question->additional_info = $extra_info;
						$questions[] = $this_question;
						$num_want -= 1;
					}
				}
				
				else {
					// Get required info.
					$album_name = $data_items[$data_keys]["_displayName"];
					$url = $data_items[$data_keys]["_url"];
					$privacy = $data_items[$data_keys]["_privacy"];
					$time = $data_items[$data_keys]["_published"];
					$cover_photo = $data_items[$data_keys]["_coverPhoto"]["_fullImage"];
					$timestamp = parse_prisoner_time($time);
					$extra_info = array();
					$extra_info["num_photos"] = $data_items[$key]["_count"];
						
					// Create question object and add it to our list.
					$this_question = new Question(TYPE_ALBUM, $album_name);
					$this_question->timestamp = $timestamp;
					$this_question->privacy_of_data = strtoupper($privacy);
					$this_question->image = $cover_photo;
					$this_question->permalink = $url;
					$this_question->additional_info = $extra_info;
					$questions[] = $this_question;
					$num_want -= 1;
				}
				
				break;
				
			case TYPE_PHOTO:
				if (is_array($data_keys)) {
					foreach ($data_keys as $key) {
						// Get required info.
						$photo_name = $data_items[$key]["_displayName"];
						$url = $data_items[$key]["_url"];
						$photo = $data_items[$key]["_image"]["_fullImage"];
						$time = $data_items[$key]["_published"];
						$timestamp = parse_prisoner_time($time);
					
						// Create question object and add it to our list.
						$this_question = new Question(TYPE_PHOTO, $photo_name);
						$this_question->timestamp = $timestamp;
						$this_question->image = $photo;
						$this_question->permalink = $url;
						$questions[] = $this_question;
						$num_want -= 1;
					}
				}
				
				else {
					// Get required info.
					$photo_name = $data_items[$data_keys]["_displayName"];
					$url = $data_items[$data_keys]["_url"];
					$photo = $data_items[$data_keys]["_image"]["_fullImage"];
					$time = $data_items[$data_keys]["_published"];
					$timestamp = parse_prisoner_time($time);
						
					// Create question object and add it to our list.
					$this_question = new Question(TYPE_PHOTO, $photo_name);
					$this_question->timestamp = $timestamp;
					$this_question->image = $photo;
					$this_question->permalink = $url;
					$questions[] = $this_question;
					$num_want -= 1;
				}
				
				break;
		}
		
		// General case clean-up.
		if ($question_type != TYPE_PROFILE) {
			foreach ($data_keys as $key) {
				unset($data_items[$key]);
			}
		}
		
		// Loop through the array of questions and check for null / empty questions.
		foreach ($questions as &$question) {
			if (empty($question)) {
				$question = new Question(TYPE_ERROR, "");
				$question->response = true;
				log_msg("Note: Detected empty question. Inserting placeholder.");
			}
		}
		
		log_msg(" - Returned " . count($questions) . " questions.");
		$_SESSION["question_info"][$question_type] = $question_info_obj;
		return $questions;
	}
	
	
	/**
	 * Calculates the data available for the supplied type and returns the amount of compensation that is required.
	 * If the number of pieces of data we want is greater than the number we have, this means that compensation is
	 * needed.
	 * @param int $question_type The question type to get questions for.
	 * @return int The amount of compensation that is required. (0 if we have more pieces of data than we need)
	 */
	function calculate_available_data($question_type) {
		// Globals.
		global $PROFILE_INFO_KEYS;
		
		$question_info_obj = &$_SESSION["question_info"][$question_type];
		log_msg("Calculating available data for " . $question_info_obj->friendly_name);
		
		// Special case for profile info.
		if ($question_type == TYPE_PROFILE) {
			$question_info_obj->num_have = count($PROFILE_INFO_KEYS);
		}
		
		// General case.
		else {
			$question_info_obj->num_have = count($question_info_obj->data);
		}
		
		// Calculate difference.
		$num_want = $question_info_obj->num_want;
		$num_have = $question_info_obj->num_have;
		$diff = $num_have - $num_want;
		$question_info_obj->num_spare = $diff;
		log_msg(" - Want: " . $num_want . ", Have: " . $num_have . ", Difference: " . $diff);
		
		// Return the amount of compensation required.
		if ($diff < 0) {
			$question_info_obj->num_want = $num_have;
			return abs($diff);
		}
		
		// We have plenty of data.
		else {
			return 0;
		}
	}
	
	
	/**
	 * Calculates the total number of data items available on the participant's profile.
	 * @return number The total number of data items available.
	 */
	function calculate_total_data() {
		$total_data_items = 0;
		
		foreach ($_SESSION["question_info"] as &$question_info_obj) {
			$total_data_items += $question_info_obj->num_have;
		}
		
		return $total_data_items;
	}
	
	
	/**
	 * Gets the meta data associated with the supplied question type.
	 * This function can be used to help with the "Results" section at the end of the questionnaire.
	 * Returns an array containing the number of questions of the supplied type, the number of times the participant 
	 * was willing to share info of the supplied type and, finally, the percentage of shares.
	 * @param int $question_type The question type to get info about.
	 * @return array An array of meta data about the question.
	 */
	function get_question_meta_data($question_type) {
		$questions = $_SESSION["questions"];
		$num_of_type = 0;
		$shares = 0;
		
		// Loop through each question.
		foreach ($questions as $question) {
			if ($question->type == $question_type) {
				$num_of_type ++;
				
				if ($question->response == true) {
					$shares ++;
				}
			}
		}
		
		$percentage_shares = ($shares / $num_of_type) * 100;
		$percentage_shares = round($percentage_shares, 2);
		
		// Return array of results.
		$to_return = array();
		$to_return[] = $num_of_type;
		$to_return[] = $shares;
		$to_return[] = $percentage_shares;
		return $to_return;
	}
	
	
	/**
	 * Commits the results to the PRISONER framework and performs a number of essential housekeeping duties.
	 * In order, the participant's "Finished" flag is set in our database, ensuring they can't take the study again,
	 * any information stored about them in their session is deleted to avoid holding onto sensitive data, the .group file
	 * is reset, so the next participant gets assigned the right group and finally, the participant's results are POSTed to
	 * PRISONER.
	 */
	function commit_participant_results($enc_facebook_id) {
		// Globals.
		global $db;
		
		// Get required info from session.
		$participant_id = $_SESSION["participant_id"];
		$participant_group = $_SESSION["group"];
		$prisoner_participant_id = $_SESSION["prisoner_participant_id"];
		$prisoner_session_id = $_SESSION["prisoner_session_id"];
		$questions = $_SESSION["questions"];
		log_msg("Committing participant results.");
		
		// Set finished flag in database.
		$is_finished = true;
		$query = "UPDATE participant SET is_finished = '$is_finished' WHERE facebook_id = '$enc_facebook_id';";
		log_msg("Query: " . $query);
		$result = mysqli_query($db, $query);
			
		if (!$result) {
			log_msg("Error - Failed to set is_finished flag: " . mysqli_error($db));
		}
		
		else {
			log_msg("Successfully set is_finished flag.");
		}
		
		// Remove any stored session data.
		$session_data = NULL;
		$query = "UPDATE participant SET session_data = '$session_data' WHERE facebook_id = '$enc_facebook_id';";
		log_msg("Query: " . $query);
		$result = mysqli_query($db, $query);
			
		if (!$result) {
			log_msg("Error - Failed to purge session data: " . mysqli_error($db));
		}
		
		else {
			log_msg("Successfully purged session data.");
		}
		
		// Reset group assignment.
		if ($participant_group == GROUP_1) {
			$fh = fopen(GROUP_FILE_LOCATION, "w");
 			fwrite($fh, "1");
 			fclose($fh);
		}
		
		else {
			$deleted_ok = unlink(GROUP_FILE_LOCATION);
		}
		
		// Commit results to PRISONER database.
		$init_url = PRISONER_URL;
		$post_url = $init_url . "/post" . "?PRISession=" . $prisoner_session_id;
		
		foreach ($questions as $question) {
			$type = $question->type;
			$privacy = $question->privacy_of_data;
			$response = $question->response;
			
			if (empty($privacy)) {
				$privacy = "N/A";
			}
			
			// Build response data.
			$question_response["participant_id"] = $prisoner_participant_id;
			$question_response["group_id"] = $participant_group;
			$question_response["info_type"] = $type;
			$question_response["privacy"] = $privacy;
			$question_response["response"] = $response;
			
			$post_data["schema"] = "response";
			$post_data["response"] = json_encode($question_response);
			
			$ch = curl_init();
			curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
			curl_setopt($ch, CURLOPT_POSTFIELDS, $post_data);
			curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
			curl_setopt($ch, CURLOPT_URL, $post_url);
			$post_response = curl_exec($ch);
			curl_close($ch);
			
			log_msg("Commit question response. (Participant: " . $prisoner_participant_id . ", Group: " . $participant_group . 
			", Type: " . $type . ", Privacy: " . $privacy . ", Response: " . $response . ")");
		}
	}
	
	
	/**
	 * Checks whether or not the requested data is available from PRISONER yet.
	 * @param str $data_type_str PRISONER name of the data to check for.
	 * @param str $session_id PRISONER session ID.
	 * @return mixed Returns false if the data is not yet available, otherwise the data response is returned.
	 */
	function check_data_availability($data_type_str, $session_id) {
		$response = get_response("/get/Facebook/" . $data_type_str . "/session:Facebook.id", $session_id, false, true);
		
		// Is there a JSON object in the response?
		if (empty($response)) {
			return false;
		} 
		
		else {
			return $response;
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
	 * Given a valid key, this function will return a question object for that piece of information.
	 * This function is necessary because, unlike data such as photo albums and status updates, profile information
	 * has a certain amount of context. For example, we cannot use generic phrases for the questions.
	 * This function therefore creates questions that have appropriate preambles and so on.
	 * @param array $profile_info Array of profile information.
	 * @param string $data_key Key to generate question for.
	 */
	function get_profile_question($profile_info, $data_key) {
		// Get the URL of the participant's profile.
		$url = $profile_info["_url"];
		
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
				
				$this_question->permalink = $url;
				return $this_question;
				break;
			
			// Last name.
			case "_lastName":
				return get_profile_question_obj($profile_info, $data_key, "Your last name is");
				break;
			
			// Birthday.
			case "_birthday":
				$this_question = get_profile_question_obj($profile_info, $data_key, "Your date of birth is");
				
				// No info.
				if (!$this_question) {
					$this_question = new Question(TYPE_PROFILE, "");
					$this_question->custom_question_text = "You have not added your date of birth to Facebook";
				}
				
				// If birthday info exists, remember to format it correctly.
				else {
					$birthday_timestamp = parse_prisoner_time($this_question->text_data);
					$birthday = date("l j F Y", $birthday_timestamp);
					$this_question->text_data = $birthday;
				}
				
				$this_question->permalink = $url;
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
				
				$this_question->permalink = $url;
				return $this_question;
				break;
			
			// Political views.
			case "_politicalViews":
				$this_question = get_profile_question_obj($profile_info, $data_key, "Your political alignment is");
				
				if (!$this_question) {
					$this_question = new Question(TYPE_PROFILE, "");
					$this_question->custom_question_text = "You have not added information about your political alignment to Facebook";
				}
				
				$this_question->permalink = $url;
				return $this_question;
				break;
			
			// Religious views.
			case "_religion":
				$this_question = get_profile_question_obj($profile_info, $data_key, "You are");
				
				if (!$this_question) {
					$this_question = new Question(TYPE_PROFILE, "");
					$this_question->custom_question_text = "You have not added information about your religion to Facebook";
				}
				
				$this_question->permalink = $url;
				return $this_question;
				break;
			
			// Relationship status.
			case "_relationshipStatus":
				$this_question = get_profile_question_obj($profile_info, $data_key, "You are");
				
			if (!$this_question) {
				$this_question = new Question(TYPE_PROFILE, "");
				$this_question->custom_question_text = "Information about your relationship status is not available";
			}
			
			$this_question->permalink = $url;
			return $this_question;
			break;
		
			// Interested in.
			case "_interestedIn":
				$this_question = get_profile_question_obj($profile_info, $data_key, "You are interested in");
			
				if (!$this_question) {
					$this_question = new Question(TYPE_PROFILE, "");
					$this_question->custom_question_text = "Information about your sexual orientation is not available";
				}
				
				else {
					$friendly_list = get_friendly_list($this_question->text_data, true);
					$this_question->text_data = $friendly_list;
				}
				
				$this_question->permalink = $url;
				return $this_question;
				break;
			
			// Languages.
			case "_languages":
				$this_question = get_profile_question_obj($profile_info, $data_key, "You know");
						
				if (!$this_question) {
					$this_question = new Question(TYPE_PROFILE, "");
					$this_question->custom_question_text = "Information about the languages you know is not available";
				}
				
				else {
					$friendly_list = get_friendly_list($this_question->text_data, true);
					$this_question->text_data = $friendly_list;
				}
				
				$this_question->permalink = $url;
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
				$date = date("l j F Y", $last_update);
				$time = date("H:i", $last_update);
				$last_update = $date . "</strong> at <strong>" . $time;
				$this_question = new Question(TYPE_PROFILE, $last_update);
				$this_question->custom_question_text = "You last updated your profile information on";
				$this_question->permalink = $url;
				return $this_question;
				break;
			
			// Profile picture.
			case "_image":
				$profile_pic = $profile_info[$data_key]["_fullImage"];
				$profile_pic = "<img alt='Profile Picture' src='" . $profile_pic . "' />";
				$this_question = new Question(TYPE_PROFILE, $profile_pic);
				$this_question->custom_question_text = "Your current profile picture can be seen below";
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
					$this_question->permalink = $url;
					return $this_question;
				}
				
				// No info available.
				else {
					$this_question = new Question(TYPE_PROFILE, "");
					$this_question->custom_question_text = "You have not added information about your hometown to Facebook.";
					$this_question->permalink = $url;
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
					$this_question->permalink = $url;
					return $this_question;
				}
				
				// No info available.
				else {
					$this_question = new Question(TYPE_PROFILE, "");
					$this_question->custom_question_text = "You have not added information about your current location to Facebook";
					$this_question->permalink = $url;
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
					$this_question->permalink = $url;
					return $this_question;
				}
				
				// No info available.
				else {
					$this_question = new Question(TYPE_PROFILE, "");
					$this_question->custom_question_text = "Information about your significant other is not available on Facebook";
					$this_question->permalink = $url;
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
					$this_question->permalink = $url;
					return $this_question;
				}
				
				// No info available.
				else {
					$this_question = new Question(TYPE_PROFILE, "");
					$this_question->custom_question_text = "You have not added information about your education history to Facebook";
					$this_question->permalink = $url;
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
						$this_question->permalink = $url;
						return $this_question;
					}
				
					// No info available.
					else {
						$this_question = new Question(TYPE_PROFILE, "");
						$this_question->custom_question_text = "You have not added information about your work history to Facebook";
						$this_question->permalink = $url;
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
		$url = $profile_info["_url"];
		
		// No data exists.
		if (empty($data_value)) {
			return false;
		}
		
		// Data exists.
		else {
			// Create and return question object.
			$this_question = new Question(TYPE_PROFILE, $data_value);
			$this_question->custom_question_text = $question_text;
			$this_question->permalink = $url;
			
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
		$permalink = $question->permalink;
		
		// Generate markup.
		$markup = "<div class='statement'>";
		$markup .= "<div class='statement_info'><p>Question #" . $question_number . " / " . NUM_QUESTIONS . "</p></div>" . "\n";
		
		switch ($type) {
			case TYPE_PROFILE:
				$data_item = $question->text_data;
				$question_text = $question->custom_question_text;
				
				// Is this the user's profile pic?
				if (strpos($data_item, "<img alt") !== false) {
					$markup .= "<p>" . $question_text . ".</p>" . $data_item;
				}
				
				// General case.
				else {
					$markup .= "<p>" . $question_text . " <strong>" . $data_item . "</strong>. <br />";
					$markup .= "Click <a href='" . $permalink . "' target='_blank'>here</a> to view your Facebook profile.  (Opens in a new tab / window)</p>";
				}
				
				break;
			
			case TYPE_FRIEND:
				$markup .= "<p>You are friends with <strong>" . $text_data . "</strong>. <br />" .
				"Click <a href='" . $permalink . "' target='_blank'>here</a> to view this friend's Facebook profile. (Opens in a new tab / window)</p>";
				break;
			
			case TYPE_LIKE:
				$markup .= "<p>You like <strong>" . $text_data . "</strong>. <br />" .
				"Click <a href='" . $permalink . "' target='_blank'>here</a> to view this like / interest's Facebook page. (Opens in a new tab / window)</p>";
				break;
			
			case TYPE_CHECKIN:
				$date = date("l j F Y", $question->timestamp);
				$time = date("H:i", $question->timestamp);
				$markup .= "<p>You were tagged at <strong>" . $text_data . "</strong> on <strong>" . $date . "</strong> at <strong>" .
				$time . "</strong>.</p>";
				break;
			
			case TYPE_STATUS:
				$date = date("l j F Y", $question->timestamp);
				$time = date("H:i", $question->timestamp);
				$markup .= "<p>You posted saying <em>&quot;" . $text_data . "&quot;</em> on <strong>" . $date . "</strong> at <strong>" .
				$time . "</strong>. <br />" .
				"Click <a href='" . $permalink . "' target='_blank'>here</a> to view this status update on Facebook. (Opens in a new tab / window)</p>";
				break;
			
			case TYPE_ALBUM:
				$date = date("l j F Y", $question->timestamp);
				$time = date("H:i", $question->timestamp);
				$filename = "tmp_images/" . date("U") . "_" . rand() . ".jpg";
				$num_photos = $question->additional_info["num_photos"];
				$image_address = $question->image;
				
				$image_adjuster = new resize($image_address);
				$image_adjuster->resizeImage(700, 700);
				$image_adjuster->saveImage($filename, 75);
				$markup .= "<p>You added photos to an album called <strong>" . $text_data . "</strong> on <strong>" . $date . "</strong> at " .
				"<strong>" . $time . "</strong>. There are <strong>" . $num_photos . "</strong> photos in the album. The album's cover photo can " .
				"be seen below. <br />" .
				"Click <a href='" . $permalink . "' target='_blank'>here</a> to see this album on Facebook. (Opens in a new tab / window)</p>";
				$markup .= "<img alt='Facebook Photo' src='" . $filename . "' />";
				break;
			
			case TYPE_PHOTO:
				$date = date("l j F Y", $question->timestamp);
				$filename = "tmp_images/" . date("U") . "_" . rand() . ".jpg";
				$image_address = $question->image;
				$image_info = getimagesize($image_address);
				$image_width = $image_info["width"];
				$image_height = $image_info["height"];
				$landscape = true;
				$preferred_width = 700;
				$preferred_height = 700;
				
				if ($image_height > $image_width) {
					$landscape = false;
					$preferred_width = 350;
					$preferred_height = 500;
				}
				
				$image_adjuster = new resize($image_address);
				$image_adjuster->resizeImage($preferred_width, $preferred_height);
				$image_adjuster->saveImage($filename, 75);
				
				$markup .= "<p>A photo you are tagged in can be seen below. <br />" .
				"Click <a href='" . $permalink . "' target='_blank'>here</a> to see at this photo on Facebook. (Opens in a new tab / window)</p>";
				$markup .= "<img alt='Facebook Photo' src='" . $filename . "' />";
				break;
			
			case TYPE_ERROR:
				$markup .= "<p>An error occurred trying to load this question, please click <strong>Next Question</strong> to continue.</p>";
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