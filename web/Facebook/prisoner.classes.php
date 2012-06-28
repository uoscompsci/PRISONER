<?php
	
	// Include any required components.
	include_once("prisoner.constants.php");
	include_once("prisoner.database.php");
	
	
	/**
	 * Simple class to hold information about a type / category of Facebook information. (Eg: Profile info, Check-ins)
	 * Records the number of pieces of that info we want, the number we have, and any spare.
	 * Used mainly internally to divide up questions between categories in the event some category doesn't have enough
	 * items.
	 */
	class InfoType {
		var $name = NULL;
		var $num_want = 0;
		var $num_have = 0;
		var $num_spare = 0;
		var $mismatch = 0;
		var $type = NULL;
		
		
		/**
		 * Constructs a new InfoType object with the supplied name.
		 * @param string $name_to_set The InfoType's name.
		 */
		function __construct($name_to_set, $type_to_set) {
			$this->name = $name_to_set;
			$this->type = $type_to_set;
		}
	}
	
	
	/**
	 * A question object. At their simplest level, questions consist of some text data, a type and a response.
	 * Different types of question may also use additional attributes such as image data and timestamps.
	 */
	class Question {
		var $type = NULL;
		var $custom_question_text = NULL;
		var $text_data = NULL;
		var $image = NULL;
		var $timestamp = NULL;
		var $privacy_of_data = NULL;
		var $response = NULL;
		var $additional_info = NULL;
		
		
		/**
		 * Constructs a new Question object.
		 * @param int $type The question's type.
		 * @param string The question's text data.
		 */
		function __construct($type, $text_data) {
			$this->type = $type;
			$this->text_data = $text_data;
		}
	}
	
?>