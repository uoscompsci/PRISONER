<?php
	
	
	/**
	 * Takes a URL as a string and accesses it, returning the response.
	 * Any cookies returned are also included in the response.
	 * @param String $url
	 * @return String
	 */	
	function get_data($url) {
		// Initialise cURL.
		$ch = curl_init();
		
		// Set options.
		curl_setopt($ch, CURLOPT_HEADER, 1);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
		curl_setopt($ch, CURLOPT_URL, $url);
		
		// Access address and close connection.
		$data = curl_exec($ch);
		curl_close($ch);
		
		return $data;
	}
	
	session_start();
	
	// Set some initial constants and variables.
	$PRISONER_ADDRESS = "http://127.0.0.1:5000";
	
	// Get initial response from PRISONER.
	$pri_response = get_data($PRISONER_ADDRESS);
	
	// Use RegEx to parse response for the session cookie.
	$matches = NULL;
	$cookie_regex = "/^Set-Cookie: (.*?);/m";
	preg_match($cookie_regex, $pri_response, $matches);
	
	// Extract session ID.
	$session_cookie = $matches[1];
	$session_cookie_array = explode("=", $session_cookie);
	$session_id = $session_cookie_array[1];
	$_SESSION["PRISession"] = $session_cookie;
	
	// Set cookie.
	setcookie("PRISession", $session_id);
	
	// Output confirmation.
	echo "<p>Performed initial handshake with PRISONER.</p>";
	echo "<p>Retrieved and set session ID: " . $session_id . "</p>";
	
	// Try and initiate experiment.
	echo "<p>Executing POST request.</p>";
	$ch = curl_init();
	
	// Set POST data.
	$post_data["policy"] = "http://localhost/prisoner/xml/fb_privacy_policy_test.xml";
	$post_data["design"] = "http://localhost/prisoner/xml/fb_exp_design_test.xml";
	$post_data["participant"] = "1";
	$post_data["providers"] = "Facebook";
	
	// Set options.
	curl_setopt($ch, CURLOPT_COOKIE, $session_cookie);
	curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
	curl_setopt($ch, CURLOPT_POSTFIELDS, $post_data);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt($ch, CURLOPT_URL, $PRISONER_ADDRESS . "/begin?callback=localhost/prisoner/exp.php");
	
	// Access address and close connection.
	$data = curl_exec($ch);
	curl_close($ch);
	
	// Returned data will be URL the participant must go to. Append callback and print.
	$callback_uri = "http://localhost/prisoner/exp.php";
	$callback_uri = urlencode($callback_uri);
	$data = $data . "&callback=" . $callback_uri;
	echo "<p>Sign in here: <a href=\"" . $data . "\">Facebook</a></p>";
	
?>