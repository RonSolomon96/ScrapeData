import sys
import requests
from Post import Post


def main():
    # receive arguments
    arg = sys.argv
    if len(arg) <= 1:
        raise Exception("not valid number of arguments")

    p = Post(arg[1])

    inp = "p"
    while inp != "e":
        # get the html response
        try:
            response = requests.get(p.url)

            if response.status_code == 200:
                # Scrape posts from the HTML we got
                p.scrape_posts(response.text)
                inp = "e"


        except requests.RequestException as e:

            print(f"An error occurred: {e}")

            retry = input("Do you want to try again? (y/n): ")

            if retry.lower() != 'y':
                inp = "e"  # Exit the loop if the user doesn't want to retry


if __name__ == "__main__":
    main()
