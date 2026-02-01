Django Email Auto-Responder
My first commit of this repo is jsut a python file and virtual environment but later i have integerated Django for UX and Database.
A simple Django-based email automation system built for clarity and resume value.

## Features
- Login with email + app password (no Django auth)
- Fetch unread emails using IMAP
- Rule-based auto-replies using SMTP
- Manual STOP control during execution
- Run-specific overview of processed emails
- Clean service-layer architecture
App password is your mail password it something that can be obtained my turning on Two step Authorization.

## Tech Stack
- Python
- Django
- IMAP (imaplib)
- SMTP (smtplib)
- SQLite (default Django DB)

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
1. Enable Gmail IMAP
2. Generate App Password
3. Run:
   ```bash
   python manage.py runserver

That's it page loads with unseen mails and their status.

## 🎥 Demo Flow (how YOU should show it)

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

