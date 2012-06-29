<?php

	// Include any required components.
	include_once("prisoner.constants.php");
	include_once("prisoner.core.php");
	
	// Start a session on the server.
	//ob_start();
	//session_start();
	
	$db = mysqli_connect(DATABASE_HOST, DATABASE_USER, DATABASE_PASS, DATABASE_NAME);
	
	// Connection error.
	if (!$db) {
		log_msg("Error - Couldn't connect to database server: " . mysqli_error());
	}
	
	else {
		log_msg("Successfully connected to database.");
	}
	
	
	/**
	 * Encrypts the supplied data with 256-bit AES.
	 * @param string $to_encrypt The string to encrypt.
	 * @return string A base 64 encoded version of the encrypted string.
	 */
	function encrypt($to_encrypt) {
		return trim(base64_encode(mcrypt_encrypt(MCRYPT_RIJNDAEL_256, SALT, $to_encrypt, MCRYPT_MODE_ECB, 
		mcrypt_create_iv(mcrypt_get_iv_size(MCRYPT_RIJNDAEL_256, MCRYPT_MODE_ECB), MCRYPT_RAND))));
	}
	
	
	/**
	 * Decrypts the supplied string.
	 * @param string $to_decrypt The AES-encrypted data to decrypt.
	 * @return string The original string.
	 */
	function decrypt($to_decrypt) {
		return trim(mcrypt_decrypt(MCRYPT_RIJNDAEL_256, SALT, base64_decode($to_decrypt), MCRYPT_MODE_ECB, 
		mcrypt_create_iv(mcrypt_get_iv_size(MCRYPT_RIJNDAEL_256, MCRYPT_MODE_ECB), MCRYPT_RAND)));
	}
	
	// Flush output buffers.
	//ob_end_flush();
?>