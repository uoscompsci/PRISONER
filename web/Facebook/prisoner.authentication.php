<?php
	
	// Include any required components.
	include_once("prisoner.constants.php");
	include_once("prisoner.core.php");
	
	
	/**
	 * Performs a handshake with the PRISONER service in order to start a session.
	 * Sets "PRISession" cookie and session variables.
	 * Returns the PRISONER session ID and a URL the user must go to in an array.
	 * ([0] = Session ID, [1] = URL)
	 */
	function start_prisoner_session() {
		// URLs we need to authenticate.
		$init_url = PRISONER_URL;
		$begin_url = $init_url . "/begin?callback=" . urlencode(CALLBACK_URL);
		
		// Initialise a cURL session.
		$ch = curl_init();
		
		// Perform initial handshake.
		$response_headers = get_headers($init_url, 1);
		$session_id = $response_headers["PRISession"];
		
		// Get a new cURL session for the next stage.
		$ch = curl_init();
		$begin_url .= "&PRISession=" . $session_id;
		
		// Set POST data for second stage of authentication.
		$post_data["policy"] = PRIVACY_POLICY_URL;
		$post_data["design"] = EXP_DESIGN_URL;
		$post_data["participant"] = "1";
		$post_data["providers"] = "Facebook";
		
		// Set cURL options.
		curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
		curl_setopt($ch, CURLOPT_POSTFIELDS, $post_data);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
		curl_setopt($ch, CURLOPT_URL, $begin_url);
		
		// Perform second stage of authentication. (Will return a URL for the user to go to)
		$from_prisoner = curl_exec($ch);
		curl_close($ch);
		
		// Create and return response array.
		$to_return = array();
		$to_return[] = $session_id;
		$to_return[] = $from_prisoner;
		log_msg("Created new PRISONER session. (ID: " . $to_return[0] . ")");
		
		return $to_return;
	}
	
?>