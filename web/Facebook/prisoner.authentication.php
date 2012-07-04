<?php

	// Include any required components.
	include_once("prisoner.constants.php");
	include_once("prisoner.core.php");
	
	
	/**
	 * Performs a handshake with the PRISONER service in order to start a session.
	 * Sets "PRISession" cookie and session variables.
	 * Returns the PRISONER session ID and a URL the user must go to in an array.
	 * ([0] = Session ID, [1] = URL, [2] = PRISONER Participant ID)
	 */
	function start_prisoner_session() {
		// URLs we need to authenticate.
		$init_url = PRISONER_URL;
		$register_url = $init_url . "/register";
		$begin_url = $init_url . "/begin?callback=" . urlencode(CALLBACK_URL);
		
		// Generate a random name for this paticipant.
		$participant_name = rand() . "_" . date("U");
		
		// Perform initial handshake.
		$response_headers = get_headers($init_url, 1);
		$session_id = $response_headers["PRISession"];
		
		// Register this participant.
		$ch = curl_init();
		$register_url .= "?PRISession=" . $session_id;
		
		// Set POST data for second stage of authentication.
		$post_data["policy"] = PRIVACY_POLICY_URL;
		$post_data["design"] = EXP_DESIGN_URL;
		$post_data["name"] = $participant_name;
		$post_data["schema"] = "participant";
		$post_data["db"] = DB_CONNECTION_STRING;
		
		// Set cURL options.
		curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
		curl_setopt($ch, CURLOPT_POSTFIELDS, $post_data);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
		curl_setopt($ch, CURLOPT_URL, $register_url);
		
		// Perform second stage of authentication. (Will return the ID of the participant)
		$prisoner_participant_id = curl_exec($ch);
		curl_close($ch);
		
		// Get a new cURL session for the next stage. (Begin)
		$ch = curl_init();
		$begin_url .= "&PRISession=" . $session_id;
		
		// Set POST data for third stage of authentication.
		$post_data["policy"] = PRIVACY_POLICY_URL;
		$post_data["design"] = EXP_DESIGN_URL;
		$post_data["participant"] = $prisoner_participant_id;
		$post_data["providers"] = "Facebook";
		$post_data["db"] = DB_CONNECTION_STRING;
		$post_data["title"] = $_SESSION["study_title"];
		$post_data["contact"] = CONTACT_EMAIL_ADDRESS;
		
		// Set cURL options.
		curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
		curl_setopt($ch, CURLOPT_POSTFIELDS, $post_data);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
		curl_setopt($ch, CURLOPT_URL, $begin_url);
		
		// Perform third stage of authentication. (Will return a URL for the user to go to)
		$url_to_visit = curl_exec($ch);
		curl_close($ch);
		
		// Create and return response array.
		$to_return = array();
		$to_return[] = $session_id;
		$to_return[] = $url_to_visit;
		$to_return[] = $prisoner_participant_id;
		log_msg("Created new PRISONER session. (ID: " . $to_return[0] . ")");
		
		return $to_return;
	}
	
?>