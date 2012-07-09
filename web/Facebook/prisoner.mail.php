<?php
	
	// Include any required components.
	include_once("prisoner.constants.php");
	include_once("prisoner.core.php");
	include_once("prisoner.database.php");
	
	
	/**
	 * Send a voucher code to the supplied email address.
	 * @param string $email_address The email address to send the voucher code to.
	 */
	function send_voucher_code($email_address) {
		// Globals.
		global $db;
		$voucher_code = NULL;
		
		// Get a list of voucher codes.
		$query = "SELECT * FROM voucher_codes;";
		$result = mysqli_query($db, $query);
		
		// Loop through the codes and get the first unused one.
		while ($row = mysqli_fetch_array($result)) {
			$is_used = $row["is_used"];
			$voucher_code = $row["voucher_code"];
			
			// We have a new code.
			if (!$is_used) {
				// Set it to used and break out of the loop.
				$query = "UPDATE voucher_codes SET is_used = '1' WHERE voucher_code = '$voucher_code';";
				$result = mysqli_query($db, $query);
				break;
			}
		}
		
		// Compose email to send.
		$subject = "Your Amazon Gift Certificate";
		$from_addr = "Gift Certificate Mailer <no-reply@prisoner.cs.st-andrews.ac.uk>";
		$headers = "From: $from_addr" . "\r\n";
		
		$message_preamble = "Dear participant," . "\n\n" .
		"Thank you for taking part in our study, your Amazon gift certificate can be found below." . "\n" .
		"Claim code: " . $voucher_code . "\n\n";
		
		$terms = "Expiration date: 28-Jun-2013" . "\n\n" .
		"To redeem your Amazon.co.uk gift certificate, simply follow the steps below:" . "\n" . 
		"1) Select the items you wish to order, using your Shopping Basket. (Please note, you cannot use the 1-Click shopping " .
		"method when redeeming a gift certificate.)" . "\n" .
		"2) In the order form you'll see a box that says 'Have you got a gift certificate or promotional code?'" . "\n" .
		"3) Enter your claim code into the box and click the 'Apply' button." . "\n\n" .
		"You will be able to see that the value of your gift certificate has been deducted from the total cost in the order summary. " .
		"When you have successfully placed your order, the following message will be displayed: 'Thank you--we have received your order'." . "\n\n" .
		
		"The fine print:" . "\n" .
		"1) Gift certificates may only be redeemed at our Web site, http://www.amazon.co.uk, toward the purchase of products listed " .
		"in Amazon.co.uk's online catalogue. They cannot be redeemed at Amazon.com, Amazon.de, Amazon.fr, Amazon.co.jp, Amazon.ca, " . 
		"Amazon.cn or Amazon.co.uk's Trusted Partner Sites." . "\n" .
		"2) This gift certificate cannot be used to pay for Amazon.co.uk gift certificates." . "\n" .
		"3) This gift certificate has a cash redemption value of 0.001p and is not transferable or assignable." . "\n" .
		"4) Any unused balance will be placed in the recipient's gift certificate account." . "\n" .
		"5) If an order exceeds the amount of the gift certificate, the balance must be paid by credit or debit card." . "\n" .
		"6) Please use our Shopping Basket rather than our 1-Click ordering method when paying for an order with a gift certificate." . "\n" .
		"7) Gift certificates and unused portions of gift certificates expire one year from the date of issue, where " .
		"permissible under applicable law." . "\n" .
		"8) This gift certificate can be applied to an open order by visiting the relevant Order Summary page in " .
		"the 'Your Account' section of our Web site." . "\n" .
		"9) Normal Amazon.co.uk terms and conditions of purchase and for using the Amazon.co.uk Web site apply." . "\n" .
		"10) Please note that there are some products available for sale on the Amazon.co.uk website that may not be purchased " .
		"by persons under a specified age. If you are planning to give this gift certificate to someone under 18 years " .
		"of age, please ensure that they are made aware that some products are unavailable to them." . "\n\n" .
		
		"If you have any queries, please contact us at: http://www.amazon.co.uk/contact-us";
		
		$message = $message_preamble . $terms;
		$message = wordwrap($message, 120);
		
		// Send email.
		$ch = curl_init();
		$mailer_addr = "http://www.st-andrews.ac.uk/~rocksoc/cloud/mail/send_mail.php";
		
		// Set POST data for second stage of authentication.
		$post_data["to_addr"] = $email_address;
		$post_data["subject"] = $subject;
		$post_data["message"] = $message;
		$post_data["headers"] = $headers;
		
		// Set cURL options.
		curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
		curl_setopt($ch, CURLOPT_POSTFIELDS, $post_data);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
		curl_setopt($ch, CURLOPT_URL, $mailer_addr);
		
		// Send the POST request. (Can't just use mail() because it's restricted to internal addresses)
		$return_msg = curl_exec($ch);
		log_msg($return_msg);
		curl_close($ch);
	}
	
	
	function send_completion_mail() {
		$email_address = "sm2269@st-andrews.ac.uk";
		$subject = "Web Study Over";
		$message = "Hi, 100 people have finished the study.";
		$headers = "From: Web Study <no-reply@prisoner.cs.st-andrews.ac.uk>" . "\r\n";
		
		// Send email.
		$ch = curl_init();
		$mailer_addr = "http://www.st-andrews.ac.uk/~rocksoc/cloud/mail/send_mail.php";
		
		// Set POST data for second stage of authentication.
		$post_data["to_addr"] = $email_address;
		$post_data["subject"] = $subject;
		$post_data["message"] = $message;
		$post_data["headers"] = $headers;
		
		// Set cURL options.
		curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
		curl_setopt($ch, CURLOPT_POSTFIELDS, $post_data);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
		curl_setopt($ch, CURLOPT_URL, $mailer_addr);
		
		// Send the POST request. (Can't just use mail() because it's restricted to internal addresses)
		$return_msg = curl_exec($ch);
		log_msg($return_msg);
		curl_close($ch);
	}
	
?>