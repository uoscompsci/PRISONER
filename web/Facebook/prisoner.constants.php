<?php
	
	// Global variables.
	$PRISONER_URL = "http://127.0.0.1:5000";
	$CALLBACK_URL = "http://localhost/prisoner/exp_01.php";
	$PRIVACY_POLICY_URL = "http://localhost/prisoner/xml/fb_privacy_policy_test.xml";
	$EXP_DESIGN_URL = "http://localhost/prisoner/xml/fb_exp_design_test.xml";
	
	// Database.
	$DATABASE_HOST = "localhost";
	$DATABASE_USER = "sam";
	$DATABASE_PASS = "hE&rezeprestAsed";
	$DATABASE_NAME = "prisoner";
	
	$EMAIL_ADDRESS_REGEX = "/\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b/i";
	
	// Max age for a browser's cache. (User will be able to go back and change answers.)
	$CACHE_STAY_ALIVE = 60 * 30;	# 60 * 30 = 30 minutes = anticipated length of survey.
	
	// Content for group 1. (Health and social networks)
	$GROUP_1_ABOUT = "We invite you to participate in a research project about the social factors that affect your health and health care. " . "\n" .
	"We are interested in understanding how health behaviours spread through friends and social networks. For instance, if one member of your " . "\n" .
	"social network has a very healthy lifestyle, does this mean that other members of your social network will also have a healthy lifestyle? " . "\n" .
	"Similarly, if one member is depressed, does that depression spread through to other friends?" . "\n";
	$GROUP_1_TITLE = "Social Networks &amp; Health";
	
	// Content for group 2. (Information dessimination)
	$GROUP_2_ABOUT = "We invite you to participate in a research project that will help to build the next generation of mobile and wireless " . "\n" .
	"networks. We are interested in understanding how information spreads through social networks. This will help us design new networks that " . "\n" .
	"can exploit this behaviour. For instance, if we know that most information is spread (or “gossiped”) through a small number of people, " . "\n" .
	"then we can optimise our systems to take advantage of these people." . "\n";
	$GROUP_2_TITLE = "Information Dissemination In Mobile Social Networks";
	
	// Content.
	$NO_CONSENT_MESSAGE = "<p>Unfortunately you cannot participate in this study if you do not agree to the terms on the consent page. <br />" . "\n" .
	"No information has been stored about you. <br />" . "\n" .
	"To end this research study, please <strong>exit</strong> your web browser. " . "\n" .
	"(Do not just close this tab)</p>" . "\n";
	
	$STUDY_START_MESSAGE = "<p>Thank you for agreeing to take part in this study. To get started, please click the <strong>Begin</strong> " . "\n" .
	"button below.</p>" . "\n";
	
	// Definitions.
	define("GROUP_1", 1);
	define("GROUP_2", 2);
	define("SALT", "Oh Scotty doesn't know! So Don't Tell Scotty! Scotty doesn't know! Scotty doesn't know! So Don't Tell Scotty!");
	define("MYSQLI_ERROR_DUPLICATE", 1062);
	define("GROUP_FILE_LOCATION", ".group");
	
?>