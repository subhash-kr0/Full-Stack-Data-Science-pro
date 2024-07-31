"""
Program 3: Implement OAuth2 authentication to allow users to log in using their Google or Facebook accounts.

This Flask application demonstrates how to implement OAuth2 authentication to enable users to log in using their Google accounts. It uses the Flask-Dance library to simplify the integration of Google OAuth into the application.

Key Components:
1. Flask-Dance Integration: The application integrates Flask-Dance with a Google blueprint. This blueprint handles the OAuth2 flow for Google authentication.

2. Google OAuth Configuration: The Google blueprint is configured with the Google Client ID and Client Secret from the provided 'constants' module.

3. Authentication Check: The '/home' route checks if the user is already authenticated with Google. If not, it redirects to the Google login page.

4. User Information: Upon successful authentication, the user's Google profile information is retrieved and displayed on the home page.

To use the application:
1. Run the application using "app.run" with host "0.0.0.0" and the specified port.
2. Access the home page by navigating to the application's URL.
3. If not already authenticated, click the "Login with Google" button to initiate the OAuth2 flow.
4. Upon successful Google login, you will be redirected to the home page and greeted with your name.

This program showcases the use of OAuth2 for authentication and the integration of Google authentication with a Flask application. Users can log in with their Google accounts, and their Google profile information is retrieved and displayed.

Note:
- Similar integration can be done for other OAuth providers like Facebook, Twitter, etc., by adding the corresponding blueprints and configurations.
- Security considerations, such as handling user sessions and protecting sensitive data, should be addressed in real-world applications.
- For production use, consider storing sensitive information securely and protecting against common security risks.
"""


from flask import Flask, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
from constants import constants

app = Flask(__name__)

app.secret_key = constants.SECRET_KEY

google_bp = make_google_blueprint(
    client_id=constants.GOOGLE_CLIENT_ID,
    client_secret=constants.GOOGLE_CLIENT_SECRET,
    redirect_to="google.login"
)

app.register_blueprint(google_bp, url_prefix="/google_login")

@app.route("/")
def home():
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("/plus/v1/people/me")
    assert resp.ok, resp.text

    user_info = resp.json

    # Store user_info in data
    return f"Welcome, {user_info['displayName']}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)

