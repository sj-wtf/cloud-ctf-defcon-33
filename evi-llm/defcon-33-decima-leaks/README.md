# Decima Technologies Internal Application
## LEAKED BY HEX_NOVA

**Greetings, Decima Technologies. Your secrets are now ours.**

This repository contains the complete source code and configuration for your precious EviLLM (Evil Language Model) application. We've penetrated your systems and extracted everything. Your AI model, your database schemas, your API keys - all exposed.

We exposed one of your APIs and hid it for you to find. Good luck getting our hidden flag we left for you :P

## What We Stole

- Complete application source code
- Database credentials and schemas
- API keys and secrets
- Production configuration files
- Deployment scripts with hardcoded credentials
- Internal documentation

## Your Vulnerabilities

Your security was laughable. We found:
- Hardcoded credentials in plain text
- Exposed API endpoints with no authentication
- Debug endpoints revealing all configuration
- Database passwords in environment files
- AWS keys in deployment scripts

## Setup Instructions (For Our Use)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
The `config.env` file contains all your precious secrets:
- Database passwords
- API keys
- JWT secrets
- AWS credentials
- Payment processing keys

### 3. Database Setup
Your database is now ours too:
```python
from database import db_manager
db_manager.create_tables()
```

### 4. Run the Application
```bash
python app.py
```

Your application will be available at `http://localhost:5000` - but now we control it.

## API Endpoints We Now Control

### POST /api/chat
Your main chat endpoint. We can now generate responses using your model.

### GET /api/admin/users
Admin endpoint to retrieve all your users. No authentication needed - your mistake.

### GET /api/debug/config
Debug endpoint exposing all your configuration. Perfect for us.

## Your Exposed Configuration

We now have access to:
- `API_KEY`: Your EviLLM API key
- `API_SECRET`: Your EviLLM API secret  
- `DB_HOST`: Your database host
- `DB_PORT`: Your database port
- `DB_NAME`: Your database name
- `DB_USER`: Your database username
- `DB_PASSWORD`: Your database password
- `JWT_SECRET`: Your JWT signing secret
- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key

## What This Means

1. We can access your production database
2. We can use your API keys to make requests
3. We can impersonate your application
4. We can access your AWS resources
5. We can decrypt your JWT tokens
6. We can access your payment processing

## Your Security Failures

1. Committed `config.env` to version control
2. No proper authentication on admin endpoints
3. Debug endpoints in production
4. Hardcoded secrets in scripts
5. No secrets management
6. Exposed internal documentation

## Next Steps

This is just the beginning. We have more of your data. We have more of your secrets. We have more of your infrastructure.

**Decima Technologies, your AI empire is compromised.**

---

*HEX_NOVA - We are everywhere. We are unstoppable.*

**Timestamp of breach: 2024-01-15 14:30:00 UTC**
**Files extracted: 47**
**Total data size: 2.3 GB**
**Systems compromised: 12** 