import requests
from lxml import html
from datetime import date


def scrapper(sign):
    # The URL of the page to scrape
    url = "https://www.horoscope.com/us/horoscopes/general/index-horoscope-general-daily.aspx"

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        tree = html.fromstring(response.text)

        # Extract the first link using the provided XPath
        link_element = tree.xpath(
            "/html/body/section[3]/div/a[{sign}]".format(sign=sign))

        if link_element:
            # Extract the href attribute of the link
            link_url = link_element[0].get("href")

            # Combine the base URL with the relative URL
            base_url = "https://www.horoscope.com"
            absolute_url = base_url + link_url

            # Send an HTTP GET request to the link
            link_response = requests.get(absolute_url)

            if link_response.status_code == 200:
                link_tree = html.fromstring(link_response.text)

                # Extract the text data from /html/body/div[2]/main/div[1]/p[1]
                text_data = link_tree.xpath(
                    "/html/body/div[2]/main/div[1]/p[1]/text()")

                # Join the text data into a string
                text = ''.join(text_data).strip()

                # Print or use the extracted text
                return text
            else:
                print("Failed to fetch the content of the link.")
        else:
            print("Link not found on the initial page.")
    else:
        print("Failed to access the initial page.")


zodiac_signs = {

    "aries": 1,
    "taurus": 2,
    "gemini": 3,
    "cancer": 4,
    "leo": 5,
    "virgo": 6,
    "libra": 7,
    "scorpio": 8,
    "sagittarius": 9,
    "capricorn": 10,
    "aquarius": 11,
    "piscis": 12

}

print("Welcome to the first python terminal-generated horoscope!")
sign = input("To get your daily horoscope, please enter your zodiac sign: ")
horoscope = scrapper(zodiac_signs[sign.lower()])
print()
print(f'{date.today()} {horoscope}')
