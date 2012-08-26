import utils
import os
import sys
import re
from textile import textile
from email.parser import Parser
from mako.template import Template
from mako.lookup import TemplateLookup

class Post():
    def __init__(self, title=None, timestamp=None, msg=None, link=None):
        self.title = title
        self.author = config['name']
        self.timestamp = timestamp
        self.msg = msg
        self.filename = self.create_filename(self.title)
        self.link = config['base url']+self.filename

    def create_filename(self, title):
        # replace all non-word chars with '-'
        link = re.sub(r'\W+', '-', title.lower())
        # replace multiple '-' with single '-', use only first 30 chars
        return re.sub(r'-+', '-', link).strip('-')[:30]+".html"

def publish():    
    # store all posts
    posts = []

    # path to our rsync-ed data
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), config['data'])

    # traverse the entire data dir
    for root, dir, files in os.walk(path):
        for file in files:
            with open(os.path.join(root, file)) as fh:
                post = parse_mail(fh)
                if post:
                    make_post(post)
                    posts.append(post)

    make_index(posts)

def parse_mail(mail):
    mail = Parser().parse(mail)

    # this works for me, might be break for stupid^Wweirdly configured clients
    sender = mail['from'].split('<')[0].strip()

    if config['name'] != sender:
        return

    post = Post(mail['subject'], mail['date'])

    for part in mail.walk():
        # i support only plain text, sending stupid^Wfancy html mails wont work
        if part.get_content_type() != "text/plain":
            continue
        # don't publish replies; pretty hackish -- is there a better alternative?
        if 'Re: [devlog]' in mail['subject']:
            continue
        post.msg = textile(part.get_payload(decode=True))

    return post

def make_post(post):
    # path to templates
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    template_path = os.path.join(template_path, 'base.html')
    mytemplate = Template(filename=template_path, module_directory='/tmp/mako_modules')
    
    #path to output file
    outfh_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'posts')
    outfh_path = os.path.join(outfh_path, post.filename)
    
    with open(outfh_path, 'w') as outfh:
        outfh.write(mytemplate.render(post=post))

def make_index(posts):
    # path to templates
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    template_path = os.path.join(template_path, 'index.html')
    mytemplate = Template(filename=template_path, module_directory='/tmp/mako_modules')
    
    #path to output file
    outfh_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')
    
    with open(outfh_path, 'w') as outfh:
        outfh.write(mytemplate.render(posts=posts))

if __name__ == '__main__':
    # parse the config file
    config = utils.parse_config("config.ini")

    publish()
