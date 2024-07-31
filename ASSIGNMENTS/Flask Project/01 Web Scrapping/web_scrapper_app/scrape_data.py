"""
Program 1: Build a Flask app that scrapes data from multiple websites and displays it on your site.
You can try to scrap websites like YouTube , Amazon and show data on output pages and deploy it on cloud
platform .

"""

from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from constants import constants
import os

app = Flask(__name__)
app.config['STATIC_FOLDER'] = '/images'

save_dir = "static/images"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

google_search_query = constants.GOOGLE_SEARCH_QUERY
google_search_url = constants.GOOGLE_SEARCH_URL


def scrape_google_images(url):
    """
    Scrape images from Google Image Search results.

    :param url: (str) The URL of the Google Image Search results page.

    Downloads and saves images to the 'static/images' directory.

    """
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        images = soup.find_all("img")

        del images[0]

        for i in images:
            image_url = i["src"]
            image_data = requests.get(image_url).content

            with open(os.path.join(save_dir, f"{google_search_query}_{images.index(i)}.jpg"), "wb") as directory:
                directory.write(image_data)


def get_image_files(directory, search_query):
    """
    Get a list of image files in the specified directory that match the Google search query.

    :param directory: (str) The directory to search for image files.
    :param search_query: (str) The Google search query string.

    :return: list[str]: A list of image file names matching the query.
    """
    image_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") and filename.startswith(search_query):
            image_files.append(filename)

    return image_files


@app.route('/')
def index():
    """
    Main route for the Flask app.

    :return:
    str: HTML page with scraped and displayed images.

    Example:
    When a user accesses the root URL, the route scrapes images from Google Image Search results and displays them on an HTML page.
    """
    scrape_google_images(google_search_url)
    google_data = get_image_files(save_dir, google_search_query)
    return render_template('index.html', image_files=google_data)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)

