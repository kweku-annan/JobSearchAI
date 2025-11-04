#!/usr/bin/env python
"""Flask application entry point"""
from flask import Flask, jsonify, request
from agent.handler import process_message
import os


app = Flask(__name__)

def extract_message_from_telex(request_data):
    """
    Extract the actual user message from Telex's JSON-RPC format.
    :param request_data: JSON-RPC from Telex
    :return:
    """
    try:
        # First; try direct message field (backwards compactibility)
        if isinstance(request_data, dict) and 'message' in request_data:
            if isinstance(request_data['message'], str):
                return request_data['message']

        # Handle JSON-RPC format from Telex
        if 'params' in request_data:
            params = request_data['params']

            if 'message' in params:
                message_obj = params['message']

                # Extract from parts array
                if 'parts' in message_obj:
                    parts = message_obj['parts']

                    # Look for the first text part (latest user message)
                    for part in parts:
                        if part.get('kind') == 'text':
                            text = part.get('text', '').strip()
                            # Skip HTML tags and empty messages
                            if text and not text.startswith('<'):
                                return text
        return None
    except Exception as e:
        print(f"Error extracting message: {e}")
        return None

app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    message = request.args.get('message', '')
    if not message:
        return jsonify({
            "status": "healthy",
            "agent": "JobSearchAI",
            "version": "1.0.0"
        }), 200

@app.route('/a2a/jobsearchai', methods=['POST', 'GET'])
def jobsearchai():
    """Endpoint to process to handle Telex. A2A Protocol for Telex.im"""

    # Handle GET requests for health check
    if request.method == 'GET':
        message = request.args.get('message', '')
        if not message:
            return jsonify({
                "status": "healthy",
                "agent": "JobInsightAI",
                "version": "1.0"
            }), 200

    # Handle POST requests for job search
    try:
        if request.method == 'POST':
            request_data = request.get_json(silent=True) or {}

            # Log for debugging
            print(f"=== INCOMING REQUEST ===")
            print(f"METHOD: {request.method}")
            print(f"Has JSON: {request_data is not None}")

            # Extract message from Telex format
            user_message = extract_message_from_telex(request_data)
            messageId = request_data.get("params", {}).get("messageId", "")


            # Fallback to query params
            if not user_message:
                user_message = request.args.get('message', '')

            print(f"Extracted message: '{user_message}'")

            if not user_message:
                return jsonify({
                    "jsonrpc": "2.0",
                    "result": {
                        "role": "assistant",
                        "parts": [
                            {
                                "kind": "text",
                                "text": "👋 Hi! I'm JobInsightAI. Tell me what job you're looking for and I'll find listings + recommend portfolio projects!\n\nExample: 'python developer' or 'backend engineer'"
                            }

                        ],
                        "messageId": messageId
                    }
                }), 200

            # Process the message
            response_text = process_message(user_message)


            print(f"Generated response (first 100 chars): {response_text[:100]}...")

            # Return in Telex JSON-RPC format
            return jsonify({
                "jsonrpc": "2.0",
                "result": {
                    "role": "assistant",
                    "parts": [
                        {
                            "kind": "text",
                            "text": response_text
                        }
                    ],
                    "messageId": messageId
                }
            }), 200

    except Exception as e:
        print(f"Error in jobsearchai endpoint: {e}")
        import traceback
        traceback.print_exc()
        request_data = request.get_json(silent=True) or {}
        messageId = request_data.get("params", {}).get("messageId", "")

        return jsonify({
            "jsonrpc": "2.0",
            "result": {
                "role": "assistant",
                "parts": [
                    {
                        "kind": "text",
                        "text": "Sorry, something went wrong. Please try again."
                    }
                ],
                "messageId": messageId
            }
        }), 200

@app.route('/', methods=['GET'])
def home():
    """Root endpoint"""
    return jsonify({
        "agent": "JobSearchAI",
        "description": "An AI-powered job search and portfolio recommendation agent.",
        "endpoint": "/a2a/jobsearchai",
        "usage": "POST {\"message\": \"<your job search query>\"}"
    }), 200
#
# if __name__ == '__main__':
#     app.run(debug=True)

