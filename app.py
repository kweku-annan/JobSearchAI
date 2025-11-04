#!/usr/bin/env python
"""Flask application entry point"""
from flask import Flask, jsonify, request
from agent.handler import process_message
import os


app = Flask(__name__)

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
            data = request.get_json(silent=True) or {}
            user_message = data.get('message', '') or request.args.get('message', '')

        if not user_message:
            return jsonify({
                "message": "Please provide a job title to search for. Example: 'python developer'"
            }), 200

        # Process the user message
        response_message = process_message(user_message)

        # Return A2A compliant response
        return jsonify({
            "message": response_message
        }), 200

    except Exception as e:
        print(f"Error in /a2a/jobsearchai endpoint: {e}")
        return jsonify({
            "message": "😞 Sorry, something went wrong while processing your request."
        }), 200 # Still return 200 for A2A compliance


@app.route('/', methods=['GET'])
def home():
    """Root endpoint"""
    return jsonify({
        "agent": "JobSearchAI",
        "description": "An AI-powered job search and portfolio recommendation agent.",
        "endpoint": "/a2a/jobsearchai",
        "usage": "POST {\"message\": \"<your job search query>\"}"
    }), 200

if __name__ == '__main__':
    app.run(debug=True)

