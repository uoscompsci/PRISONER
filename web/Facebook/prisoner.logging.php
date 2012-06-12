<?php
	
	/**
	 * Records a the supplied message in the web app's log file.
	 * @param String $to_log The message to log.
	 */
	function log_msg($to_log) {
		$date = date("d/m/Y H:i");
		$fh = fopen("prisoner_log.txt", "a");
		fwrite($fh, $date . "\t" . $to_log . "\n");
		fclose($fh);
	}
	
?>