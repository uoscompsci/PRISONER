<?php
	
	// Disable error reporting.
	error_reporting(0);
	
	// Include any required components.
	include_once("prisoner.constants.php");
	include_once("prisoner.core.php");
	
	// Loop through the temp images folder.
	$folder_path = TMP_IMAGES_FOLDER . "/*";
	$deleted_count = 0;
	
	foreach(glob($folder_path) as $file) {
		$deleted_ok = unlink($file);
		$deleted_count ++;
	}
	
	log_msg("Removed " . $deleted_count . " files from the tmp_images folder.", HOUSEKEEPING_LOG);
	
	// Rotate the study and warning log files.
	$timestamp = date("U");
	$warnings_log = "../Logs/warnings_log.txt";
	$study_log = "../Logs/study_log.txt";
	$new_warnings_log = "../Logs/" . $timestamp . "_warnings_log.txt";
	$new_study_log = "../Logs/" . $timestamp . "_study_log.txt";
		
	rename($warnings_log, $new_warnings_log);
	rename($study_log, $new_study_log);
	
	log_msg("Rotated log files.", HOUSEKEEPING_LOG);

?>