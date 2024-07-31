"""
Program 2: Create a Flask app that consumes data from external APIs and displays it to users.
Try to find an public API which will give you a data and based on that call it and deploy it on cloud platform

"""

from flask import Flask, render_template, request
from constants import constants
import requests

app = Flask(__name__)

# define the URL of the external API
api_base_url = constants.API_URL


def get_external_api_data(search_query):
    try:
        api_url = f"{api_base_url}/posts?q={search_query}"
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return []


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        search_query = request.form["search_query"]
        data = get_external_api_data(search_query)
    else:
        data = []

    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)

