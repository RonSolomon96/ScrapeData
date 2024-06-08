from datetime import datetime


# this class get all the post data and use it to display as we want
class Post:
    def __init__(self, title, author, publish_datetime, text):
        self.title = title
        self.author = author
        self.publish_datetime = self.convert_date(publish_datetime)
        self.text = text

    def to_dict(self):
        return {
            "title": self.title,
            "text": self.text,
            "published": self.publish_datetime,
            "author": self.author
        }

    # this function receive data for date and time . parse it and return the format we want
    def convert_date(self, date):
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
