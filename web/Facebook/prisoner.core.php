<?php
	
	// Include any required components.
	include_once("prisoner.constants.php");
	include_once("prisoner.database.php");
	
	/**
	 * Queries the PRISONER web service and returns a JSON object with the response.
	 * @param string $request The request to perform. (Eg: /get/Facebook/User/session:Facebook.id)
	 * @param string $cookie The PRISONER session cookie to supply the web service.
	 * @return array An associative array containing PRISONER's response.
	 */
	function get_response($request, $cookie) {		
		// Initialise a cURL session and compose the URL to query.
		$ch = curl_init();
		$query_url = PRISONER_URL . $request;
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
	
	
	/**
	 * Used to assign users to a group.
	 * We want a 50/50 distribution for each of the two groups. To do this, we look for a .group file
	 * on the server. If it does not exist, the participant is assigned to group 1 and a .group file is created. If the file
	 * already exists, the participant is assigned to group 2 and the file is deleted.
	 * @return A number representing the participant's group.
	 */
	function assign_group() {		
		// Check if the group file exists.
		$exists = file_exists(GROUP_FILE_LOCATION);
		
		if ($exists) {
			log_msg("Assigning participant to group 2.");
			$deleted_ok = unlink(GROUP_FILE_LOCATION);
			return GROUP_2;
		}
		
		else {
			log_msg("Assigning participant to group 1.");
			$fh = fopen(GROUP_FILE_LOCATION, "w");
			fwrite($fh, "1");
			fclose($fh);
			return GROUP_1;
		}
	}
	
	
	/**
	 * Records a the supplied message in the web app's log file.
	 * @param String $to_log The message to log.
	 */
	function log_msg($to_log) {
		$date = date("d/m/Y H:i:s");
		$fh = fopen(LOG_FILE, "a");
		fwrite($fh, $date . "\t" . $to_log . "\n");
		fclose($fh);
	}
	
	
	/**
	 * Queries the database to retrieve the mailing list. This is a list of email addresses of all people who
	 * indicated that they would like to receive further information regarding the research.
	 * @return A comma-separated list of email addresses.
	 */
	function get_mailing_list() {
		// Globals.
		global $db;
		
		// Compose and execute query.
		$query = "SELECT * FROM mailing_list";
		$result = mysqli_query($db, $query);
		
		if (!$result) {
			return "Error - " . mysqli_error($db);
		}
		
		else {
			$email_addresses = "";
			
			while ($row = mysqli_fetch_array($result)) {
				$email_addresses .= decrypt($row["email_address"]) . " ";
			}
			
			$email_addresses = chop($email_addresses);
			$email_addresses = str_replace(" ", ",", $email_addresses);
			return $email_addresses;
		}
	}
	

	/**
	 * Checks whether or not a participant can view the requested resource.
	 * Grabs the participant's current stage from the session and checks it against the supplied stage needed.
	 * @param int $stage_needed The stage required to access this resource.
	 * @return boolean True if the participant is at the required stage.
	 */
	function assert_can_view($stage_needed) {
		$participant_stage = $_SESSION["participant_stage"];
		
		if ($participant_stage >= $stage_needed) {
			return true;
		}
		
		else {
			return false;
		}
	}
	
	
	function load_notice($message) {
		$markup = "<div class='notice'><p><strong>Notice: </strong>" . $message . "</p></div>";
		$_SESSION["notice"] = $markup;
	}
	
	
	function get_notice() {
		return $_SESSION["notice"];
		$_SESSION["notice"] = "";
	}
	
?>