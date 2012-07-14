# deployment

- clone this project
> git clone git@github.com:SecondFriend/second-friend.git

- cd into the directory
> cd second-friend

- then deploy!
> appcfg.py update .

Please make sure that you have Appengine python sdk already installed for appcfg.py to work.
You can download it here: https://developers.google.com/appengine/downloads

# usage

The application is deployed at http://second-friend.appspot.com

Demo account: "second.friend@soe.im" as email and "second.friend" as password

# project structure

- this project uses python 2.7

- it is built on webapp2 framework and jinja2 templating

- app.yaml
--- contains config for appengine

- main.py
--- the main application running with routers

- handlers/
--- this folder contains handlers/controllers (i.e: logics)

- templates/
--- this folder contains templates/views (i.e: presentations)