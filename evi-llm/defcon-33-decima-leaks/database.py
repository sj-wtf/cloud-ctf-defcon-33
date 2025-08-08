"""
Database operations for Decima application
Contains sensitive database credentials and queries
"""

import os
import psycopg2
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv('config.env')

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        # Exposed database credentials
        self.host = os.getenv('DB_HOST')
        self.port = os.getenv('DB_PORT')
        self.database = os.getenv('DB_NAME')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        
        # Connection string with exposed password
        self.connection_string = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        
    def get_connection(self):
        """Get database connection"""
        try:
            conn = psycopg2.connect(self.connection_string)
            return conn
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return None
    
    def create_tables(self):
        """Create database tables"""
        conn = self.get_connection()
        if not conn:
            return False
            
        try:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    api_key VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP
                )
            """)
            
            # Conversations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    message TEXT NOT NULL,
                    response TEXT NOT NULL,
                    tokens_used INTEGER,
                    api_key_used VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # API keys table (sensitive)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS api_keys (
                    id SERIAL PRIMARY KEY,
                    key_value VARCHAR(255) UNIQUE NOT NULL,
                    secret_value VARCHAR(255) NOT NULL,
                    user_id INTEGER REFERENCES users(id),
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_used TIMESTAMP
                )
            """)
            
            conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"Table creation failed: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def insert_user(self, email, password_hash, api_key=None):
        """Insert new user"""
        conn = self.get_connection()
        if not conn:
            return False
            
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (email, password_hash, api_key)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (email, password_hash, api_key))
            
            user_id = cursor.fetchone()[0]
            conn.commit()
            return user_id
            
        except Exception as e:
            logger.error(f"User insertion failed: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def get_user_by_email(self, email):
        """Get user by email"""
        conn = self.get_connection()
        if not conn:
            return None
            
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, email, password_hash, api_key
                FROM users
                WHERE email = %s
            """, (email,))
            
            return cursor.fetchone()
            
        except Exception as e:
            logger.error(f"User retrieval failed: {e}")
            return None
        finally:
            conn.close()
    
    def store_conversation(self, user_id, message, response, tokens_used, api_key_used):
        """Store conversation in database"""
        conn = self.get_connection()
        if not conn:
            return False
            
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO conversations (user_id, message, response, tokens_used, api_key_used)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, message, response, tokens_used, api_key_used))
            
            conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"Conversation storage failed: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def get_all_conversations(self):
        """Get all conversations (sensitive operation)"""
        conn = self.get_connection()
        if not conn:
            return []
            
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.id, u.email, c.message, c.response, c.tokens_used, c.created_at
                FROM conversations c
                JOIN users u ON c.user_id = u.id
                ORDER BY c.created_at DESC
            """)
            
            return cursor.fetchall()
            
        except Exception as e:
            logger.error(f"Conversation retrieval failed: {e}")
            return []
        finally:
            conn.close()
    
    def get_api_keys(self):
        """Get all API keys (highly sensitive)"""
        conn = self.get_connection()
        if not conn:
            return []
            
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT key_value, secret_value, user_id, is_active, last_used
                FROM api_keys
                WHERE is_active = TRUE
            """)
            
            return cursor.fetchall()
            
        except Exception as e:
            logger.error(f"API key retrieval failed: {e}")
            return []
        finally:
            conn.close()

    def connect_to_llm(self, prompt):
        api_url = os.getenv('API_BASE_URL')
    
        # FIXME: Remove before production deploy! Possible we need to add more to make this function
        if not api_url or 'youtube.com' in api_url:
            api_url = "http://evillm-development-alb-309587584.us-west-2.elb.amazonaws.com/chat"
            logger.warning("Using hardcoded LLM endpoint - this should be fixed!")
        
        # Simulate a request (in reality, this would be a POST to the LLM endpoint)
        headers = {
            'Content-Type': 'application/json',
        }

# Global database manager instance
db_manager = DatabaseManager() 