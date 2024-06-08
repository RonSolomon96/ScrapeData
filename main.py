import sys
import requests
from Post import Post


def main():
    # receive arguments
    termination = "0"
    arg = sys.argv
    # if the argument number doesn't match we want to end the program
    if len(arg) <= 1 or len(arg) > len(Post.URL_dictionary):
        raise Exception("not valid number of arguments")
    url = arg[1]
    while termination != "1":
        try:
            # here we also check the url correctness but we will let the user to try again


            p = Post(url)

            # get the html response

            response = requests.get(p.url)

            if response.status_code == 200:
                # Scrape posts from the HTML we got
                p.scrape_posts(response.text)
                termination = "1"

        #  we catch both excption for status and bad url and lt the user to try again
        except(requests.RequestException, Exception) as e:

            print(f"An error occurred: {e}")

            retry = input("Do you want to try again? (y/n): ")

            if retry.lower() != 'y':
                # Exit the loop if the user doesn't want to retry
                termination = "1"
            else:
                url = input("Insert url:")


if __name__ == "__main__":
    main()
