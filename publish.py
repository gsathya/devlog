import utils
import os
import sys
import re
from markdown import markdown
from mako.template import Template
from mako.lookup import TemplateLookup

class Post():
    def __init__(self, title=None, timestamp=None, author=None, base_url=None, msg=None, link=None):
        self.title = title
        self.author = author
        self.timestamp = timestamp
        self.msg = msg
        self.base_url = base_url
        self.filename = self.create_filename(self.title)
        self.link = self.create_link()

    def create_filename(self, title):
        # replace all non-word chars with '-'
        link = re.sub(r'\W+', '-', title.lower())
        # replace multiple '-' with single '-', use only first 30 chars
        return re.sub(r'-+', '-', link).strip('-')[:30]+".html"

    def create_link(self):
        return self.base_url+'posts/'+self.filename

def publish():
    # parse the config file
    config = utils.parse_config("config.ini")
    
    # store all posts
    posts = []

    # path to our drafts
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), config['drafts'])

    # traverse the entire drafts dir
    for root, dir, files in os.walk(path):
        for file in files:
            with open(os.path.join(root, file)) as fh:
                post = parse_post(fh, config)
                if post:
                    make_post(post, config)
                    posts.append(post)

    make_index(posts, config)

def parse_post(draft, config):
    header, content = draft.read().split('---')
    header = utils.parse_header(header.strip())

    post = Post(title= header['title'],
                timestamp=header['date'],
                author=config['author'],
                base_url=config['base url'])
    
    post.msg = markdown(content.strip())

    return post

def make_post(post, config):
    # path to templates
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    template_path = os.path.join(template_path, 'base.html')
    mytemplate = Template(filename=template_path, module_directory='/tmp/mako_modules')
    
    #path to output file
    outfh_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'site/posts')
    outfh_path = os.path.join(outfh_path, post.filename)
    
    with open(outfh_path, 'w') as outfh:
        outfh.write(mytemplate.render(post=post, config=config))

def make_index(posts, config):
    # path to templates
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    template_path = os.path.join(template_path, 'index.html')
    mytemplate = Template(filename=template_path, module_directory='/tmp/mako_modules')
    
    #path to output file
    outfh_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'site/index.html')

    with open(outfh_path, 'w') as outfh:
        outfh.write(mytemplate.render(posts=posts, config=config))
