# Flask Admin Portal

This is a simple Flask-based web application for user login, signup, and dashboard access. It interacts with a FastAPI backend for user authentication and management.

---

## Features
- **Login Page**: Users can log in with their email and password.
- **Signup Page**: New users can create an account.
- **Dashboard**: Authenticated users are redirected to a dashboard.

---

## Prerequisites
Before running the Flask app, ensure you have the following installed:

1. **Python** (3.8 or higher)
2. **Pip** (Python package installer)
3. **FastAPI Backend**: The FastAPI server must be running at `http://localhost:8000`.

---

## Installation and Setup

### 1. Clone or Download the Project
Download or clone this repository to your local machine.

```bash
git clone <repository_url>
cd your_project_directory

2. Set Up a Virtual Environment (Optional but Recommended)

Create and activate a virtual environment to isolate dependencies.

python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows

3. Install Required Packages

Install the necessary Python packages using pip:

pip install flask requests

4. Set Up the FastAPI Backend

    Navigate to the FastAPI project directory.
    Start the FastAPI backend server using the following command:

    uvicorn backend.main:app --reload

    Confirm that the FastAPI server is available at http://localhost:8000.

Running the Flask App
1. Navigate to the Flask Project Directory

Make sure you are in the directory containing app.py.
2. Start the Flask Server

Run the following command to start the server:

python app.py

3. Access the Application

Open your web browser and visit the following URLs:

    Login Page: http://127.0.0.1:5000/login
    Signup Page: http://127.0.0.1:5000/signup
    Dashboard: Redirected here after a successful login.

Project Structure

your_project/
├── app.py             # Main Flask application
└── templates/         # HTML templates for Flask
    ├── login.html     # Login page
    ├── signup.html    # Signup page
    └── dashboard.html # Dashboard page

Troubleshooting
Common Errors

    jinja2.exceptions.TemplateNotFound:
        Ensure the templates folder exists and contains login.html, signup.html, and dashboard.html.
        Verify the templates folder is in the same directory as app.py.

    ConnectionError:
        Ensure the FastAPI backend is running and accessible at http://localhost:8000.

    Session Errors:
        Ensure app.secret_key in app.py is set to a secure random string.

    Debug Mode:
        To enable debug mode, run:

        FLASK_ENV=development python app.py

Example Flow

    Signup:
        Navigate to http://127.0.0.1:5000/signup.
        Enter your email and password, then click "Sign Up."

    Login:
        Navigate to http://127.0.0.1:5000/login.
        Enter your email and password, then click "Login."
        If successful, you will be redirected to the dashboard.

    Dashboard:
        The dashboard is a placeholder page for future features.

