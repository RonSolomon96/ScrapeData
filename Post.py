from datetime import datetime
import re
import json

# this pot class contains utils functions and data to handle posts data from different websites
class Post:
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

    def __init__(self, url):
        self.url_check(url)
        self.url = url

    @staticmethod
    def url_check(url):
        if url not in Post.URL_dictionary.keys():
            raise Exception("This is not a valid URL")




    def scrape_posts(self, html_content):
        posts_list = []
        # Find all matches of the post pattern
        posts = re.findall(self.URL_dictionary[self.url]["post_pattern"], html_content, re.DOTALL)

        for post_content in posts:
            # Extract post metadata
            title_match = re.search(self.URL_dictionary[self.url]["title_pattern"], post_content, re.DOTALL)
            author_match = re.search(self.URL_dictionary[self.url]["author_pattern"], post_content)

            datetime_match = re.search(self.URL_dictionary[self.url]["datetime_pattern"], post_content, re.DOTALL)
            text_match = re.search(self.URL_dictionary[self.url]["text_pattern"], post_content, re.DOTALL)
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
            text = re.sub(r'<.*?>', '', text).strip()

            # Create Post instance
            post_info = self.to_dict(title, text, publish_datetime, author)
            posts_list.append(post_info)
        name = "Post" + self.URL_dictionary[self.url]["ID"] + ".json"
        self.save_posts_to_json(posts_list, name)
        print("succeded! the file " + name + " has been updated ")

    @staticmethod
    def save_posts_to_json(posts, filename):
        json_list = []
        for post in posts:
            json_list.append(post)
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(json_list, file, ensure_ascii=False, indent=4)

    @staticmethod
    def to_dict(title, text, publish_datetime, author):
        return {
            "title": title,
            "text": text,
            "published": publish_datetime,
            "author": author
        }

    # this function receive data for date and time . parse it and return the format we want
    @staticmethod
    def convert_date(date):
        date_formats = [
            "%a %d %b '%y, %I:%M%p",
            "%a %b %d, %Y %I:%M %p"
        ]

        for date_format in date_formats:
            try:
                parsed_date = datetime.strptime(date, date_format)
                return parsed_date.strftime("%Y/%m/%d %H:%M")
            except ValueError:
                continue
        raise ValueError("Date format not recognized")
