<?php
	
	
	class QuestionType {
		var $friendly_name = NULL;
		var $prisoner_name = NULL;
		var $session_name = NULL;
		var $type = NULL;
		var $data = NULL;
		var $generated_questions = false;
		var $loaded_data = false;
		var $num_want = 0;
		var $num_have = 0;
		var $num_spare = 0;
		
		
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