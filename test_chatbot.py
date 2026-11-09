"""
test_chatbot.py - Automated Unit & Integration Tests
CodeAlpha Python Programming Internship - Task 4: Basic Chatbot

Runs comprehensive test suites using Python's standard library unittest:
1. Core Chatbot Logic & Rule-Based Intent Matching (chatbot.py)
2. Normalization, Validation, and Edge Cases
3. Flask Endpoints, Status Codes, and JSON Validation (app.py)
"""

import json
import unittest

from app import app
from chatbot import get_bot_response, normalize_text


class TestChatbotLogic(unittest.TestCase):
    """Unit tests for chatbot.py core rule matching and normalization."""

    def test_all_required_greeting_inputs(self):
        """Verifies every specific greeting input from the project requirements."""
        required_greetings = [
            "hi",
            "hello",
            "hey",
            "good morning",
            "good afternoon",
            "good evening",
            "HELLO",
            "Hey!",
            "Hi there",
            "Good Morning!"
        ]
        for phrase in required_greetings:
            with self.subTest(phrase=phrase):
                response = get_bot_response(phrase)
                self.assertEqual(response, "Hi! Nice to meet you. How can I help you?")

    def test_all_required_wellbeing_inputs(self):
        """Verifies every specific well-being input from the project requirements."""
        required_wellbeing = [
            "how are you",
            "how are you doing",
            "HOW ARE YOU",
            "How are you?",
            "how are you doing today"
        ]
        for phrase in required_wellbeing:
            with self.subTest(phrase=phrase):
                response = get_bot_response(phrase)
                self.assertEqual(response, "I'm fine, thanks! How are you?")

    def test_all_required_identity_inputs(self):
        """Verifies identity questions return the predefined identity response."""
        required_identity = [
            "who are you",
            "what is your name",
            "what's your name",
            "whats your name",
            "Who are you?",
            "WHAT IS YOUR NAME?"
        ]
        for phrase in required_identity:
            with self.subTest(phrase=phrase):
                response = get_bot_response(phrase)
                self.assertEqual(response, "I'm PyBot, a simple rule-based chatbot built with Python.")

    def test_all_required_capabilities_inputs(self):
        """Verifies capabilities/help inquiries return the predefined capabilities response."""
        required_capabilities = [
            "what can you do",
            "help",
            "what do you do",
            "What can you do?",
            "HELP!",
            "What do you do?"
        ]
        expected_response = (
            "I can respond to simple greetings, answer a few predefined questions, "
            "and demonstrate a basic Python chatbot."
        )
        for phrase in required_capabilities:
            with self.subTest(phrase=phrase):
                response = get_bot_response(phrase)
                self.assertEqual(response, expected_response)

    def test_all_required_thanks_inputs(self):
        """Verifies thank-you messages return the predefined gratitude response."""
        required_thanks = [
            "thanks",
            "thank you",
            "Thanks!",
            "Thank you very much!",
            "THANK YOU"
        ]
        for phrase in required_thanks:
            with self.subTest(phrase=phrase):
                response = get_bot_response(phrase)
                self.assertEqual(response, "You're welcome!")

    def test_all_required_goodbye_inputs(self):
        """Verifies goodbye messages return the predefined departure response."""
        required_goodbye = [
            "bye",
            "goodbye",
            "see you",
            "Bye!",
            "GOODBYE",
            "See you later"
        ]
        for phrase in required_goodbye:
            with self.subTest(phrase=phrase):
                response = get_bot_response(phrase)
                self.assertEqual(response, "Goodbye! Have a great day!")

    def test_unknown_fallback(self):
        """Verifies unrecognized inputs trigger the fallback guidance response."""
        unknown_inputs = [
            "What is the weather in Paris?",
            "Tell me a joke",
            "quantum mechanics",
            "123456789",
            "xyz random query"
        ]
        expected_unknown = (
            "Sorry, I don't understand that message yet. "
            "Try saying hello, asking how I am, or typing help."
        )
        for phrase in unknown_inputs:
            with self.subTest(phrase=phrase):
                response = get_bot_response(phrase)
                self.assertEqual(response, expected_unknown)

    def test_case_insensitivity(self):
        """Verifies that upper, lower, and mixed cases yield the identical response."""
        self.assertEqual(get_bot_response("HELLO"), get_bot_response("hello"))
        self.assertEqual(get_bot_response("hOw ArE yOu"), get_bot_response("how are you"))
        self.assertEqual(get_bot_response("BYE"), get_bot_response("bye"))
        self.assertEqual(get_bot_response("WHAT CAN YOU DO"), get_bot_response("what can you do"))

    def test_whitespace_and_punctuation(self):
        """Verifies leading/trailing whitespace and punctuation are stripped cleanly."""
        self.assertEqual(get_bot_response("   hello   "), "Hi! Nice to meet you. How can I help you?")
        self.assertEqual(get_bot_response("hello?!?!"), "Hi! Nice to meet you. How can I help you?")
        self.assertEqual(get_bot_response("...bye..."), "Goodbye! Have a great day!")
        self.assertEqual(get_bot_response("  how are you?  "), "I'm fine, thanks! How are you?")

    def test_substring_boundary_safety(self):
        """Verifies that unrelated words containing substrings do not trigger false positives."""
        # 'shine' should NOT trigger 'hi'
        expected_unknown = (
            "Sorry, I don't understand that message yet. "
            "Try saying hello, asking how I am, or typing help."
        )
        self.assertEqual(get_bot_response("shine"), expected_unknown)
        self.assertEqual(get_bot_response("machine"), expected_unknown)

    def test_empty_and_invalid_inputs(self):
        """Verifies that empty strings or non-string types raise appropriate exceptions."""
        with self.assertRaises(ValueError):
            get_bot_response("")
        with self.assertRaises(ValueError):
            get_bot_response("    ")
        with self.assertRaises(TypeError):
            get_bot_response(None)  # type: ignore
        with self.assertRaises(TypeError):
            get_bot_response(12345)  # type: ignore
        with self.assertRaises(TypeError):
            get_bot_response(["hello"])  # type: ignore


class TestFlaskBackend(unittest.TestCase):
    """Integration tests for Flask HTTP routes in app.py."""

    def setUp(self):
        """Initializes the Flask test client."""
        self.app = app
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def test_health_endpoint(self):
        """Verifies GET /health returns HTTP 200 with healthy status."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data.get("status"), "healthy")
        self.assertEqual(data.get("service"), "PyBot Chatbot")
        self.assertEqual(data.get("version"), "1.0.0")

    def test_index_page(self):
        """Verifies GET / serves the HTML user interface."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"PyBot", response.data)
        self.assertIn(b"chat-card", response.data)

    def test_chat_success(self):
        """Verifies POST /chat with valid message returns HTTP 200 and expected bot response."""
        payload = {"message": "hello"}
        response = self.client.post(
            "/chat",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data.get("status"), "success")
        self.assertEqual(data.get("response"), "Hi! Nice to meet you. How can I help you?")

    def test_chat_boundary_500_chars(self):
        """Verifies POST /chat with exactly 500 characters succeeds."""
        # 500-char message that doesn't match known intents should trigger unknown fallback
        payload = {"message": "a" * 500}
        response = self.client.post(
            "/chat",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data.get("status"), "success")

    def test_chat_missing_message(self):
        """Verifies POST /chat with missing 'message' key returns HTTP 400 error."""
        payload = {"text": "hello"}
        response = self.client.post(
            "/chat",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data.get("status"), "error")
        self.assertIn("Missing required field 'message'", data.get("error"))

    def test_chat_empty_message(self):
        """Verifies POST /chat with empty message returns HTTP 400 error."""
        payload = {"message": "   "}
        response = self.client.post(
            "/chat",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data.get("status"), "error")
        self.assertIn("cannot be empty", data.get("error"))

    def test_chat_non_string_message(self):
        """Verifies POST /chat with non-string payload returns HTTP 400 error."""
        payload = {"message": 9999}
        response = self.client.post(
            "/chat",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data.get("status"), "error")
        self.assertIn("must be a text string", data.get("error"))

    def test_chat_excessive_length(self):
        """Verifies POST /chat with message exceeding 500 chars returns HTTP 400 error."""
        payload = {"message": "a" * 501}
        response = self.client.post(
            "/chat",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data.get("status"), "error")
        self.assertIn("exceeds maximum allowed length", data.get("error"))

    def test_chat_non_json_request(self):
        """Verifies POST /chat without application/json Content-Type returns HTTP 400."""
        response = self.client.post(
            "/chat",
            data="message=hello",
            content_type="application/x-www-form-urlencoded"
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data.get("status"), "error")
        self.assertIn("Content-Type: application/json", data.get("error"))

    def test_chat_malformed_json_payload(self):
        """Verifies POST /chat with malformed JSON string returns HTTP 400."""
        response = self.client.post(
            "/chat",
            data="{not-a-valid-json",
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data.get("status"), "error")

    def test_chat_method_not_allowed(self):
        """Verifies GET /chat returns HTTP 405 Method Not Allowed."""
        response = self.client.get("/chat")
        self.assertEqual(response.status_code, 405)
        data = response.get_json()
        self.assertEqual(data.get("status"), "error")

    def test_chat_resource_not_found(self):
        """Verifies GET /chat/nonexistent returns HTTP 404 JSON response."""
        response = self.client.get("/chat/nonexistent")
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data.get("status"), "error")


if __name__ == "__main__":
    unittest.main()
