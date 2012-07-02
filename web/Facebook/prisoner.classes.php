<?php
	
	
	/**
	 * A QuestionType object is used to represent all the necessary information needed to generate questions of its type.
	 */
	class QuestionType {
		var $friendly_name = NULL;	# A friendly description of this type of question. (Eg: Profile info)
		var $prisoner_name = NULL;	# The name PRISONER uses for this type of info.
		var $session_name = NULL;
		var $type = NULL;	# Internal ID for this type of info.
		var $data = NULL;	# Facebook data for this type of info. (JSON)
		var $generated_questions = false;	# Flag indicating whether or not questions have been generated for this type.
		var $loaded_data = false;	# Flag indicating whether or not data has been loaded for this type.
		var $num_want = 0;	# The number of questions of this type we want.
		var $num_have = 0;	# The number of pieces of info of this type that we have.
		var $num_spare = 0;	# The number of spare pieces of info.
		
		
		function __construct($friendly_name, $type, $prisoner_name, $session_name) {
			$this->friendly_name = $friendly_name;
			$this->type = $type;
			$this->prisoner_name = $prisoner_name;
			$this->session_name = $session_name;
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
		var $permalink = NULL;
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