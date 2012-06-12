<?php
	
	// Include any required components.
	include_once("prisoner.constants.php");
	include_once("prisoner.logging.php");
	
	/**
	 * Queries the PRISONER web service and returns a JSON object with the response.
	 * @param string $request The request to perform. (Eg: /get/Facebook/User/session:Facebook.id)
	 * @param string $cookie The PRISONER session cookie to supply the web service.
	 * @return array An associative array containing PRISONER's response.
	 */
	function get_response($request, $cookie) {
		// Globals.
		global $PRISONER_URL;
		
		// Initialise a cURL session and compose the URL to query.
		$ch = curl_init();
		$query_url = $PRISONER_URL . $request;
		log_msg("Executing query: " . $query_url);
		
		// Set options.
		curl_setopt($ch, CURLOPT_COOKIE, $cookie);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
		curl_setopt($ch, CURLOPT_URL, $query_url);
		
		// Access address and close connection.
		$from_prisoner = curl_exec($ch);
		curl_close($ch);
		
		// Parse response as JSON and return.
		return json_decode($from_prisoner, true);
	}
	
?>