"""
app.py - Flask Web Application for PyBot
CodeAlpha Python Programming Internship - Task 4: Basic Chatbot

Routes:
- GET  /        : Renders the single-page chat interface (templates/index.html)
- POST /chat    : Validates user input and returns rule-based bot response as JSON
- GET  /health  : System health check endpoint for testing and monitoring
"""

import argparse
import os
import sys
from flask import Flask, jsonify, render_template, request
from chatbot import get_bot_response

# Maximum allowed message length to protect against buffer/payload abuse
MAX_MESSAGE_LENGTH = 500

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static"
)

# Limit incoming request payload size (16 KB max for chat JSON)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024


@app.route("/", methods=["GET"])
def index():
    """Serves the main single-page chat interface."""
    return render_template("index.html")


@app.route("/health", methods=["GET"])
def health():
    """Returns application health status for monitoring and automated verification."""
    return jsonify({
        "status": "healthy",
        "service": "PyBot Chatbot",
        "version": "1.0.0"
    }), 200


@app.route("/chat", methods=["POST"])
def chat():
    """
    Processes user chat messages via HTTP POST.

    Expects JSON body:
        {"message": "Hello"}

    Returns JSON body:
        {"status": "success", "response": "Hi! Nice to meet you. How can I help you?"}
    """
    # 1. Validate that the request Content-Type is application/json
    if not request.is_json:
        return jsonify({
            "status": "error",
            "error": "Invalid request format. Request body must be valid JSON with 'Content-Type: application/json'."
        }), 400

    # 2. Parse JSON payload safely
    try:
        data = request.get_json(silent=True)
    except Exception:
        return jsonify({
            "status": "error",
            "error": "Malformed JSON payload."
        }), 400

    if data is None or not isinstance(data, dict):
        return jsonify({
            "status": "error",
            "error": "Request body must be a valid JSON object."
        }), 400

    # 3. Check for existence of 'message' key
    if "message" not in data:
        return jsonify({
            "status": "error",
            "error": "Missing required field 'message' in JSON payload."
        }), 400

    raw_message = data.get("message")

    # 4. Validate data type
    if not isinstance(raw_message, str):
        return jsonify({
            "status": "error",
            "error": "Field 'message' must be a text string."
        }), 400

    # 5. Validate length and content
    trimmed_message = raw_message.strip()
    if not trimmed_message:
        return jsonify({
            "status": "error",
            "error": "Message cannot be empty or contain only whitespace."
        }), 400

    if len(raw_message) > MAX_MESSAGE_LENGTH:
        return jsonify({
            "status": "error",
            "error": f"Message exceeds maximum allowed length of {MAX_MESSAGE_LENGTH} characters."
        }), 400

    # 6. Execute rule-based response logic
    try:
        bot_response = get_bot_response(trimmed_message)
        return jsonify({
            "status": "success",
            "response": bot_response
        }), 200
    except ValueError as ve:
        return jsonify({
            "status": "error",
            "error": str(ve)
        }), 400
    except Exception:
        # Never expose internal stack traces or server details
        return jsonify({
            "status": "error",
            "error": "An internal error occurred while processing the message."
        }), 500


@app.errorhandler(400)
def bad_request(error):
    """Handle 400 Bad Request."""
    return jsonify({
        "status": "error",
        "error": "Bad request."
    }), 400


@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found."""
    if request.path.startswith("/chat") or request.path.startswith("/health"):
        return jsonify({
            "status": "error",
            "error": "The requested resource was not found."
        }), 404
    return render_template("index.html"), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 Method Not Allowed."""
    return jsonify({
        "status": "error",
        "error": "HTTP method not allowed for this route."
    }), 405


@app.errorhandler(500)
def server_error(error):
    """Handle 500 Internal Server Error securely."""
    return jsonify({
        "status": "error",
        "error": "Internal server error."
    }), 500


def main():
    """Parses command-line arguments and launches the Flask development server."""
    parser = argparse.ArgumentParser(description="Run PyBot Flask Server")
    parser.add_argument("--host", default=os.environ.get("HOST", "0.0.0.0"), help="Host IP to bind (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "3000")), help="Port to listen on (default: 3000)")
    parser.add_argument("--debug", action="store_true", default=False, help="Run in debug mode")

    args, _ = parser.parse_known_args()

    print(f"Starting PyBot Flask server on http://{args.host}:{args.port}")
    print("Note: This Flask development server is intended for development and local testing.")
    # Run the server
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
