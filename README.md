Django Email Auto-Responder
My first commit of this repo is just a python file and virtual environment but later I have integerated Django for UX and Database. Later a web application that connects to a Gmail account using Google OAuth and automatically replies to unread emails based on simple rules.
The project focuses on clean backend logic, real API integration.

## Features
- Login with email + app password (no Django auth) later it changed to Google Oauth login.
- Fetch unread emails from INBOX
- Rule-based auto-replies using SMTP
- Marks processed emails as read (no duplicate replies)
- Run-specific overview of processed emails
- Clean service-layer architecture
App password is your mail password it something that can be obtained my turning on Two step Authorization.

## Tech Stack
- Python
- Django
- Gmail API
- Google OAuth 2.0
- SQLite (for development)
- HTML + CSS (Django templates)

## Architecture
- Single Django app
- Service layer for email logic
- One execution = one run (UUID-based)
- No background workers or async processing

## Auto-Reply Rules
- Emails containing keywords like:
  - "internship"
  - "interview"
- Others are skipped
I want to narrow this skipped factor if you have any idea give a PRs.

## Why No Authentication?
This project focuses on controlled execution clarity rather than multi-user complexity.

## How to Run
User clicks Login with Google
Google OAuth permission is granted
App stores OAuth token in session
User clicks Run Email Automation

App:

Fetches unread emails from Inbox
Sends auto-replies
Marks emails as read
Saves logs to database
User can view email history in the overview page

## Demo Flow (how YOU should show it)

1. Open login page  
2. Enter email + app password  
3. Click **Login / Run**  
4. Show processing page  
5. Show **STOP** button  
6. Click **Overview**  
7. Show DB-backed table  

##  Optional Next Upgrades 

- AI reply generation (Gemini / OpenAI)
- Confidence-based reply skipping
- Attachment detection
- Background execution

Designed to run:

Synchronously (simple mode)

Can be extended to background processing if needed

Focused on clarity, not overengineering

## Auto-reply logic (example)

Emails containing words like:

internship, interview, offer, application
→ Get a formal reply

Other non-system emails
→ Get a polite acknowledgement

System / no-reply emails
→ Marked for manual review

## Security Notes

No passwords are stored

OAuth tokens are kept only in session

Secrets are managed using environment variables

.env, virtual environments, and secrets are ignored via .gitignore

## How to run locally (high level)

Clone the repository

Create and activate a virtual environment

Install dependencies

Set Google OAuth credentials as environment variables

Run Django server

Open browser at http://127.0.0.1:8000/

(Detailed setup can be added later if needed)

This project demonstrates(take aways):

Real OAuth integration
Third-party API usage
Backend request handling
Session management
Debugging real-world issues
Clean Django project structure
Suitable for internship and junior backend roles.