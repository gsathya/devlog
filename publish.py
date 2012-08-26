import utils
import os
import sys
from textile import textile
from email.parser import Parser
from mako.template import Template
from mako.lookup import TemplateLookup

class Post():
    def __init__(self, filename, title, author, timestamp):
        self.filename = filename
        self.title = title
        self.author = author
        self.timestamp = timestamp

def publish():
    # parse the config file
    config = utils.parse_config("config.ini")

    # path to our rsync-ed data
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), config['data'])

    # traverse the entire data dir
    for root, dir, files in os.walk(path):
        for file in files:
            with open(os.path.join(root, file)) as fh:
                parse_mail(fh)

def parse_mail(mail):
    mail = Parser().parse(mail)
    for part in mail.walk():
        # i support only plain text, sending stupid^Wfancy html mails wont work
        if part.get_content_type() != "text/plain":
            continue
        # don't publish replies; pretty hackish -- is there a better alternative?
        if 'Re: [devlog]' in mail['subject']:
            continue
        msg = textile(part.get_payload(decode=True))

def make_index(posts):
    pass

if __name__ == '__main__':
    publish()
