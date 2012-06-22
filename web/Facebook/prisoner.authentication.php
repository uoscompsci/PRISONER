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
		
		// Set options for initial handshake.
		curl_setopt($ch, CURLOPT_HEADER, 1);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
		curl_setopt($ch, CURLOPT_URL, $init_url);
		
		// Perform initial handshake.
		$from_prisoner = curl_exec($ch);
		curl_close($ch);
		
		// Use RegEx to extract the session ID from PRISONER's response.
		$matches = NULL;
		$cookie_regex = "/^Set-Cookie: (.*?);/m";
		preg_match($cookie_regex, $from_prisoner, $matches);
		
		// Grab ID from cookie and add it to the session. (And assign it to a cookie)
		$session_cookie = $matches[1];
		$session_cookie_array = explode("=", $session_cookie);
		$session_id = $session_cookie_array[1];
		$_SESSION["PRISession"] = $session_cookie;
		setcookie("PRISession", $session_id);
		
		// Get a new cURL session for the next stage.
		$ch = curl_init();
		
		// Set POST data for second stage of authentication.
		$post_data["policy"] = PRIVACY_POLICY_URL;
		$post_data["design"] = EXP_DESIGN_URL;
		$post_data["participant"] = "1";
		$post_data["providers"] = "Facebook";
		
		// Set cURL options.
		curl_setopt($ch, CURLOPT_COOKIE, $session_cookie);
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
	
	
	/**
	 * This function sets a session on *our* end using the information provided by PRISONER.
	 * This function is needed because our local session will get destroyed when the user is redirected to the
	 * PRISONER web app to sign into services.
	 * This should be called on the first page PRISONER redirects to.
	 */
	function set_session() {
		// Grab data from the cookie PRISONER returned.
		$session_id = $_COOKIE["PRISession"];
		$session_cookie = "PRISession=" . $session_id;
		
		// Set this info in our own server session.
		$_SESSION["PRISession_ID"] = $session_id;
		$_SESSION["PRISession_Cookie"] = $session_cookie;
	}
	
?>