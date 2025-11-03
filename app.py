#!/usr/bin/env python
"""Flask application entry point and setup"""
from flask import Flask, jsonify, request
from agent.handler import process_message



app = Flask(__name__)


@app.route('/a2a/jobsearchai', methods=['POST'])
def jobsearchai():
    """Handles incoming webhook requests"""
    message = request.args.get('message', '')

    response_message = process_message(message)
    return jsonify(response_message), 200

#
# if __name__ == "__main__":
#     app.run(debug=True)
