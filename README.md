# ScrapeData

Web Scraping with Python
This Python script demonstrates how to perform web scraping using the requests library. It fetches the HTML content of a webpage, extracts information from it, and performs some processing.

Before running the script make sure you have python 3.
requests library

imports 
import re
import json
import sys
import requests

Clone the repository to your local machine:
to run use
python main.py "url"

the argument to the script must be 1 valid url 

The script sends an HTTP GET request to a specified URL using the requests.get() function.

Status Code Check: It checks if the status code of the HTTP response is 200, indicating a successful request.

HTML Parsing: If the request is successful, it extracts the HTML content of the webpage using the response.text and regex.

Error Handling: The script includes error handling using a try-except block to catch potential exceptions that may occur during the HTTP request.