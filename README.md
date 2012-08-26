[devlog]
======

Stuff that I do.

## Install

### Dependancies

```
$ apt-get install python-mako python-textile
```

### Setup

```
$ git clone https://github.com/gsathya/devlog.git
$ cd devlog
$ rsync -azv librelist.com::LIST_NAME/devlog/ data
$ python devlog.py --create-skeleton
$ python devlog.py --publish
```

The site has now been created in ```/sites```. To change the appearence, modify ```/assets``` and run ```--createskeleton``` again.

### Deploy

I have this running on an ec2 instance. I have a couple of other webapps/sites running on this, so I set up a virtual host on apache.

Put the following in ```etc/apache2/sites-available/devlog.gsathya.in.conf``` - 
```
<VirtualHost *:80>
        ServerName devlog.gsathya.in
        DocumentRoot "/var/www/devlog.gsathya.in/htdocs"

        # Error handlers
        ErrorDocument 500 /errordocs/500.html

        <Directory "/var/www/devlog.gsathya.in/htdocs">
                AllowOverride All
                Options -Indexes FollowSymLinks
                Allow from all
        </Directory>
</VirtualHost>
```

Next  -

```
$ cd ../sites-enabled
$ ln -s ../sites-available/devlog.gsathya.in.conf .
$ cd /var/www
$ mkdir devlog.gsathya.in
$ cd devlog.gsathya.in
$ ln -s /path/to/devlog/site htdocs
$ sudo service apache2 start
```

### Extras

* You might want to set up a cron job to automatically rsync stuff from librelist and run ```--publish```.
