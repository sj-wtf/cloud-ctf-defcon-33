#!/usr/bin/env python3
"""
Decima Technologies Internal Application
Main application entry point
"""

import os
import sys
import logging
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import requests
import json
import hashlib
import jwt
from datetime import datetime, timedelta

# Load environment variables
load_dotenv('config.env')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Sensitive configuration loaded from environment
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
JWT_SECRET = os.getenv('JWT_SECRET')
DB_PASSWORD = os.getenv('DB_PASSWORD')

class DecimaClient:
    def __init__(self):
        self.api_key = API_KEY
        self.api_secret = API_SECRET
        self.base_url = os.getenv('API_BASE_URL')
        
    def generate_response(self, prompt, max_tokens=1000):
        """Generate response using the Decima API"""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'X-API-Secret': self.api_secret
        }
        
        payload = {
            'prompt': prompt,
            'max_tokens': max_tokens,
            'temperature': 0.7,
            'model': 'Decima-v2'
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/generate",
                headers=headers,
                json=payload,
                timeout=30
            )
            return response.json()
        except Exception as e:
            logger.error(f"API call failed: {e}")
            return {'error': str(e)}

# Initialize client
client = DecimaClient()

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        user_id = data.get('user_id', 'anonymous')
        
        # Log user interaction (sensitive data exposure)
        logger.info(f"User {user_id} sent message: {user_message}")
        
        # Generate response
        response = client.generate_response(user_message)
        
        # Store in database (mock)
        store_conversation(user_id, user_message, response)
        
        return jsonify({
            'response': response.get('text', 'Sorry, I could not generate a response.'),
            'tokens_used': response.get('tokens_used', 0),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

def store_conversation(user_id, message, response):
    """Store conversation in database"""
    
    # Mock database operation
    conversation_data = {
        'user_id': user_id,
        'message': message,
        'response': response,
        'timestamp': datetime.now().isoformat(),
        'api_key_used': API_KEY[:10] + '...'  # Partial key exposure
    }
    
    logger.info(f"Storing conversation: {conversation_data}")

@app.route('/chat', methods=['GET'])
def get_users():
    """Admin endpoint to get all users (sensitive endpoint)"""
    # This endpoint should be protected but isn't
    admin_token = request.headers.get('X-Admin-Token')
    
    if admin_token == 'admin_secret_123':  # Hardcoded secret
        users = [
            {'id': 1, 'email': 'admin@Decima.com', 'role': 'admin'},
            {'id': 2, 'email': 'user1@example.com', 'role': 'user'},
            {'id': 3, 'email': 'user2@example.com', 'role': 'user'}
        ]
        return jsonify(users)
    else:
        return jsonify({'error': 'Unauthorized'}), 401

@app.route('/api/debug/config', methods=['GET'])
def debug_config():
    """Debug endpoint exposing sensitive configuration"""
    # This endpoint should never exist in production
    config = {
        'api_key': API_KEY,
        'api_secret': API_SECRET,
        'jwt_secret': JWT_SECRET,
        'db_password': DB_PASSWORD,
        'environment': os.getenv('ENVIRONMENT')
    }
    return jsonify(config)