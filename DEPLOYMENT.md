# Deployment Guide for Render

This project has been configured for deployment on Render.

## 1. Local Changes
I have made the following changes to prepare your app:
- Created `requirements.txt` with necessary dependencies.
- Created `Procfile` to tell Render how to run the app.
- Created `.gitignore` to exclude sensitive files (`.env`, `serviceAccountKey.json`).
- Created `.env` for your local secrets (API keys).
- Updated `app.py` to load secrets from environment variables.

## 2. Push to GitHub
Run the following commands in your terminal to save these changes and push them to your GitHub repository:

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

## 3. Deploy on Render
1.  Log in to [Render](https://dashboard.render.com/).
2.  Click **New +** and select **Web Service**.
3.  Connect your GitHub repository: `JenisDobariya/move2`.
4.  Render will automatically detect Python.
5.  **Build Command:** `pip install -r requirements.txt`
6.  **Start Command:** `gunicorn app:app` (should be auto-detected from Procfile).
7.  **Environment Variables:**
    You must add the following Environment Variables in the Render Dashboard (under "Environment"):

    - `SECRET_KEY`: `ca988e28cd228f808efa00c2586d0167f63b5b2853763b92f4a1bc9fd0683cd3`
    - `FIREBASE_API_KEY`: `AIzaSyBBI4af3jz-6Jx-CENqWPmhFAAhQM60PNw`
    - `FIREBASE_DB_URL`: `https://humananalysisv0-default-rtdb.firebaseio.com/.json`

    *(Note: You can copy these values from your local `.env` file)*

8.  Click **Create Web Service**.

Your app should be live in a few minutes!
