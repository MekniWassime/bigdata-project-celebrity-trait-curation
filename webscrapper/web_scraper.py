import requests
import urllib
from requests_html import HTML
from requests_html import HTMLSession
from kafka import KafkaProducer
from time import sleep
from json import dumps
import sys
import os

producer = KafkaProducer(bootstrap_servers=[os.environ["KAFKA_HOST"] + ':' + os.environ["KAFKA_PORT"]],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))

def get_source(url):
    """Return the source code for the provided URL. 

    Args: 
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html. 
    """

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

def scrape_google(query):

    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?q=" + query)

    links = list(response.html.absolute_links)
    google_domains = ('https://www.google.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.')

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)

    return links

list = scrape_google("data science blogs")
def get_results(query):
    
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?q=" + query)
    
    return response
def parse_results(response, query):
    
    css_identifier_result = ".tF2Cxc"
    css_identifier_title = "h3"
    css_identifier_link = ".yuRUbf a"
    css_identifier_text = ".VwiC3b"
    
    results = response.html.find(css_identifier_result)
    
    for result in results:
        item = {
            'search': query,
            'title': result.find(css_identifier_title, first=True).text,
            'link': result.find(css_identifier_link, first=True).attrs['href'],
            'text': result.find(css_identifier_text, first=True).text
        }
        print(item)
        producer.send('webscraping-data', value=item)
        sleep(2)

def google_search(query):
    query = query.lower()
    response = get_results(query)
    parse_results(response, query)

queries = ["elon musk", "Jeff Bezos", "Bill Gates", "Warren Buffett", "Larry Ellison", "Mukesh Ambani", "Larry Page", "Sergey Brin"]
for query in queries:
    results = google_search(query)
