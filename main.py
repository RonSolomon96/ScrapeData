import re
import json
import sys
import requests
from Post import Post

# we define patterns to use for each url.

patterns2 = {
    "post_pattern": r'<div class="b-post__grid-container">(.*?)<!-- /end .b-post -->',
    "title_pattern": r'<h2.*?>(.*?)</h2>',
    "author_pattern": r'<span itemprop="name">(.*?)</span>',
    "datetime_pattern": r'<time(.*?)>(.*?)</time>',
    "text_pattern": r'<div.*? itemprop="text">\s*(.*?)\s*(<div class="h-flex-spacer'
                    r' h-margin-top-16">|<div class="post-signature restore">)',
    "ID": "2"
}

patterns1 = {
    "post_pattern": r'<div class="postbody">(.*?)</div>(?!<)',
    "title_pattern": r'<h3.*?>\s*<a.*?>(.*?)</a>',
    "author_pattern": r'class="username.*?">(.*?)</a>',
    "datetime_pattern": r'<time(.*?)>(.*?)</time>',
    "text_pattern": r'<div class="content">(.*)',
    "ID": "1"
}

# we insert th url with the matching patterns to a dictionary
URL_dictionary = {'https://forum.vbulletin.com/forum/vbulletin-3-8/vbulletin-3-8-questions-problems-and-'
                  'troubleshooting/414325-www-vs-non-www-url-causing-site-not-to-login': patterns2,
                  'http://www.phpbb.com/community/viewtopic.php?f=46&t=2159437': patterns1}

# receive arguments
arguments = sys.argv
if len(arguments) > len(URL_dictionary) or len(arguments) <= 1:
    raise Exception("not valid number of arguments")

url = arguments[1]

if url not in URL_dictionary.keys():
    raise Exception("This is not a valid URL")

regex = URL_dictionary[url]


# we save th pots to a json file
def save_posts_to_json(posts, filename):
    json_list = []
    for post in posts:
        json_list.append(post.to_dict())

    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(json_list, file, ensure_ascii=False, indent=4)


# we start scraping the HTML
def scrape_posts(html_content):
    posts_list = []
    # Find all matches of the post pattern
    posts = re.findall(URL_dictionary[url]["post_pattern"], html_content, re.DOTALL)

    for post_content in posts:
        # Extract post metadata
        title_match = re.search(URL_dictionary[url]["title_pattern"], post_content, re.DOTALL)
        author_match = re.search(URL_dictionary[url]["author_pattern"], post_content)

        datetime_match = re.search(URL_dictionary[url]["datetime_pattern"], post_content, re.DOTALL)
        text_match = re.search(URL_dictionary[url]["text_pattern"], post_content, re.DOTALL)
        # Get matched groups
        title = title_match.group(1).strip() if title_match else None
        author = author_match.group(1).strip() if author_match else None
        publish_datetime = datetime_match.group(2) if datetime_match else None
        text = text_match.group(1)
        # Replace <br> with newline
        text = text.replace('<br>', '\n')

        # Remove all other HTML tags
        # text = re.sub(r'</div>', '', text).strip()
        text = re.sub(r'<.*?>', '', text).strip()
        text = text.replace('\n', '')
        text = text.replace('\t', '')
        text = text.replace('\r', '')
        text = text.replace('&quot;', '"')
        text = re.sub(r'<a(.*?)>', ':', text).strip()
        text = re.sub(r'<.*?>', '\n', text).strip()

        # Create Post instance
        post = Post(title, author, publish_datetime, text)
        posts_list.append(post)
    name = "Post" + URL_dictionary[url]["ID"] + ".json"
    save_posts_to_json(posts_list, name)
    print("succeded! the file " + name + " has been updated ")


inp = "p"
while inp != "e":
    # get the html response
    try:
        response = requests.get(url)

        if response.status_code == 200:
            # Scrape posts from the HTML we got
            scrape_posts(response.text)
            inp = "e"


    except requests.RequestException as e:

        print(f"An error occurred: {e}")

        retry = input("Do you want to try again? (y/n): ")

        if retry.lower() != 'y':
            inp = "e"  # Exit the loop if the user doesn't want to retry
