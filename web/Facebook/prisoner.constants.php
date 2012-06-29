<?php

	// Turn off error reporting.
	//error_reporting(0);
	
	// User settings.
	$user_settings = parse_ini_file("config.ini");
	
	// Database config.
	define("DATABASE_HOST", "localhost");
	define("DATABASE_USER", "root");
	define("DATABASE_PASS", "pvnets");
	define("DATABASE_NAME", "prisoner");
	define("MYSQLI_ERROR_DUPLICATE", $user_settings["MYSQLI_ERROR_DUPLICATE"]);
	
	// Validation and security.
	define("EMAIL_ADDRESS_REGEX", "/\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b/i");
	define("SALT", "Oh Scotty doesn't know! So Don't Tell Scotty! Scotty doesn't know! Scotty doesn't know! So Don't Tell Scotty!");
	
	// PRISONER config.
	define("PRISONER_URL", "http://prisoner.cs.st-andrews.ac.uk/prisoner");
	define("CALLBACK_URL", "http://prisoner.cs.st-andrews.ac.uk/sharing/start_experiment.php");
	define("PRIVACY_POLICY_URL", "http://sm2269.host.cs.st-andrews.ac.uk/fb_privacy_policy_test.xml");
	define("EXP_DESIGN_URL", "http://sm2269.host.cs.st-andrews.ac.uk/fb_exp_design_test.xml");
	
	// Study constants.
	define("GROUP_1", 1);
	define("GROUP_2", 2);
	define("GROUP_FILE_LOCATION", ".group");
	
	define("NUM_QUESTIONS", $user_settings["NUM_QUESTIONS"]);
	define("NUM_PROFILE_QUESTIONS", $user_settings["NUM_PROFILE_QUESTIONS"]);
	define("NUM_FRIENDS_QUESTIONS", $user_settings["NUM_FRIENDS_QUESTIONS"]);
	define("NUM_LIKES_QUESTIONS", $user_settings["NUM_LIKES_QUESTIONS"]);
	define("NUM_CHECKIN_QUESTIONS", $user_settings["NUM_CHECKIN_QUESTIONS"]);
	define("NUM_STATUS_QUESTIONS", $user_settings["NUM_STATUS_QUESTIONS"]);
	define("NUM_PHOTO_ALBUM_QUESTIONS", $user_settings["NUM_PHOTO_ALBUM_QUESTIONS"]);
	define("NUM_PHOTO_QUESTIONS", $user_settings["NUM_PHOTO_QUESTIONS"]);
	
	define("NUM_PRIVACY_FRIENDS", $user_settings["NUM_PRIVACY_FRIENDS"]);
	define("NUM_PRIVACY_CUSTOM", $user_settings["NUM_PRIVACY_CUSTOM"]);
	define("NUM_PRIVACY_PUBLIC", $user_settings["NUM_PRIVACY_PUBLIC"]);
	
	define("DEBRIEFING_URL", "participant_debriefing.php");
	define("SCREENED_OUT_URL", "screened_out.php");
	
	define("STAGE_CONSENT_PAGE", 1);
	define("STAGE_NO_CONSENT", 2);
	define("STAGE_GIVEN_CONSENT", 3);
	define("STAGE_IN_STUDY", 4);
	
	// Facebook data types.
	define("TYPE_PROFILE", 0);
	define("TYPE_FRIEND", 1);
	define("TYPE_LIKE", 2);
	define("TYPE_CHECKIN", 3);
	define("TYPE_STATUS", 4);
	define("TYPE_ALBUM", 5);
	define("TYPE_PHOTO", 6);
	
	// Key names for Facebook profile information.
	$PROFILE_INFO_KEYS = array();
	$PROFILE_INFO_KEYS[] = "_username";
	$PROFILE_INFO_KEYS[] = "_displayName";
	$PROFILE_INFO_KEYS[] = "_firstName";
	$PROFILE_INFO_KEYS[] = "_middleName";
	$PROFILE_INFO_KEYS[] = "_lastName";
	$PROFILE_INFO_KEYS[] = "_gender";
	$PROFILE_INFO_KEYS[] = "_email";
	$PROFILE_INFO_KEYS[] = "_languages";
	$PROFILE_INFO_KEYS[] = "_updatedTime";
	$PROFILE_INFO_KEYS[] = "_bio";
	$PROFILE_INFO_KEYS[] = "_birthday";
	$PROFILE_INFO_KEYS[] = "_education";
	$PROFILE_INFO_KEYS[] = "_work";
	$PROFILE_INFO_KEYS[] = "_hometown";
	$PROFILE_INFO_KEYS[] = "_location";
	$PROFILE_INFO_KEYS[] = "_interestedIn";
	$PROFILE_INFO_KEYS[] = "_politicalViews";
	$PROFILE_INFO_KEYS[] = "_religion";
	$PROFILE_INFO_KEYS[] = "_relationshipStatus";
	$PROFILE_INFO_KEYS[] = "_significantOther";
	$PROFILE_INFO_KEYS[] = "_image";
	
	// Misc.
	define("CACHE_STAY_ALIVE", (60 * 60) * 60);	# 24 hours.
	define("LOG_FILE", "../Logs/study_log.txt");
	
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

?>