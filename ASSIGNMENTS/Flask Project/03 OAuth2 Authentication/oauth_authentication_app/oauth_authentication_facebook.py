"""
Program 3: Implement OAuth2 authentication to allow users to log in using their Google or Facebook accounts.

This Flask application demonstrates how to implement OAuth2 authentication to enable users to log in using their Facebook accounts. It uses the Flask-Dance library to simplify the integration of Facebook OAuth into the application.

Key Components:
1. Flask-Dance Integration: The application integrates Flask-Dance with a Facebook blueprint. This blueprint handles the OAuth2 flow for Facebook authentication.

2. Facebook OAuth Configuration: The Facebook blueprint is configured with the Facebook App ID and App Secret from the provided 'constants' module.

3. Authentication Check: The '/home' route checks if the user is already authenticated with Facebook. If not, it redirects to the Facebook login page.

4. User Information: Upon successful authentication, the user's Facebook ID, name, and email are retrieved and displayed on the home page.

To use the application:
1. Run the application using "app.run" with host "0.0.0.0" and the specified port.
2. Access the home page by navigating to the application's URL.
3. If not already authenticated, click the "Login with Facebook" button to initiate the OAuth2 flow.
4. Upon successful Facebook login, you will be redirected to the home page and greeted with your name.

This program showcases the use of OAuth2 for authentication and the integration of Facebook authentication with a Flask application. Users can log in with their Facebook accounts, and their Facebook information is retrieved and displayed.

Note:
- Similar integration can be done for other OAuth providers like Google, Twitter, etc., by adding the corresponding blueprints and configurations.
- Security considerations, such as handling user sessions and protecting sensitive data, should be addressed in real-world applications.
- For production use, consider storing sensitive information securely and protecting against common security risks.
"""


from flask import Flask, redirect, url_for
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from constants import constants

app = Flask(__name__)

app.secret_key = constants.SECRET_KEY

facebook_bp = make_facebook_blueprint(
    client_id=constants.FACEBOOK_APP_ID,
    client_secret=constants.FACEBOOK_APP_SECRET,
    redirect_to="facebook.login"
)

app.register_blueprint(facebook_bp, url_prefix="/facebook_login")


@app.route("/")
def home():
    if not facebook.authorized:
        return redirect(url_for("facebook.login"))

    resp = facebook.get("/me?fields=id,name,email")

    assert resp.ok, resp.text
    user_info = resp.json()

    return f"Welcome, {user_info['name']}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)
