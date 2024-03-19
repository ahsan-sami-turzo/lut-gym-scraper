import re

import requests
from bs4 import BeautifulSoup


def parse_data_string(s):
    numbers = re.findall(r'\d+ / \d+|\d+', s)
    functional = numbers[3]
    if ' / ' in functional:
        functional = functional.split(' / ')[0]  # take the numerator if it's a fraction
    return {
        "people_in_the_gym": numbers[0],
        "muscular_condition": numbers[1],
        "aerobic": numbers[2],
        "functional": int(functional),
    }


def get_data_from_api(url):
    # Make a GET request to the API
    response = requests.get(url)

    # The API response is a JSON, so you can convert it to a Python dictionary using .json()
    data = response.json()

    # 'content' field contains the HTML
    html_content = data['content']

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the realtime container data
    realtime_container = soup.find('div', {'id': 'realtime-container'})
    realtime_data = realtime_container.text if realtime_container else "Realtime container data not found"

    # Find the prediction container data
    prediction_container = soup.find('div', {'id': 'prediction-container'})
    prediction_data = prediction_container.text if prediction_container else "Prediction container data not found"

    # print(realtime_data)
    # print("\nPrediction Container Data:\n", prediction_data)

    parsed_data = parse_data_string(realtime_data)
    print(parsed_data)


def scrape_website(url):
    # Send a GET request to the website
    response = requests.get(url)

    # If the GET request is successful, the status code will be 200
    if response.status_code == 200:
        # Get the content of the response
        page_content = response.content

        # Create a BeautifulSoup object and specify the parser
        soup = BeautifulSoup(page_content, 'html.parser')

        # Find the 'realtime-boxes' div
        realtime_boxes = soup.find('div', class_='realtime-boxes')
        print(realtime_boxes)
        # Find all 'category-box' divs within 'realtime-boxes'
        category_boxes = realtime_boxes.find_all('div', class_='category-box')

        # Extract and print the text from each 'category-box'
        for box in category_boxes:
            print(box.get_text(strip=True))


# Use the function
# scrape_website('https://gym.lut.fi')

get_data_from_api('https://embed.gymplus.fi/v2/light/bold/lutsk')
