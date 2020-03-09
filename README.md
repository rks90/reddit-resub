reddit-resub
============

(Acknowledgements: This is forked from x89/reddit-resub. Added OAuth stuff and disabled unsubscribe from current subreddits when importing subreddits)

Export / import subreddits from a Reddit account.

Useful when you create a new user account, or if you want to drop the default subreddit subscriptions or maybe you only read /r/IAmA on a Thursday but read all the /r/Ask* subreddits on Saturday.

Set up environment
==================

 git clone https://github.com/rks90/reddit-resub
 cd reddit-resub
 virtualenv . -p python3 #if not installed use sudo apt-get install virtualenv
 source bin/activate
 pip install -r requirements.txt
```
* User account authentication setup
```
   Follow this page to setup OAuth on Reddit
   	https://alpscode.com/blog/how-to-use-reddit-api/
   Get the client-id and client-secret
   Create a pram.ini file in the running dir and add the following
   [<Username(or any name of your choosing, use this in user option below)>]
   client_id=<copy from previous step>
   client_secret=<copy from previous step>
   password=<your password>
   username=<your user name>

Usage Instructions
============

    usage: resub.py [-h] [--import] [--user USER] [--file FILE]

    Resubscribe to your old subreddits.

    optional arguments:
      -h, --help            show this help message and exit
      --import, -i          Specify -i to import to the user Default is to save
                        from a user (safe).
      --user USER, -u USER  Reddit username.
      --file FILE, -f FILE  Provide a filename to use.

Example Usage
============

* Setup OAuth on Reddit before doing the following (info below)

* Save user x89's subreddits to file abc.subs

    `python resub.py --user x89 --file abc.subs`    

* Import the subreddits listed in abc.subs to user x78

    `python resub.py --import --user x78 --file abc.subs`    

```
