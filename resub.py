#!/usr/bin/env python3

import praw
import argparse
import json

parser = argparse.ArgumentParser(
    description='Resubscribe to your old subreddits.')
parser.add_argument('--import', '-i', action="store_true",
                    help="Specify -i to import to the user, the default is to \
                    save from a user.")
parser.add_argument('--user', '-u', help="Reddit username.")
parser.add_argument('--file', '-f', help="Provide a filename to use.")


class Resub:
    def __init__(self, subscribe, user=None, filename=None):
        self._r = praw.Reddit(site_name=user,user_agent='reddit-resub 2017-05-08')
        self._user = self.get_user()

        if not filename:
            filename = '{user}.subs'.format(user=self._user)
        self._filename = filename

        if subscribe:
            print("Subscribing to subreddits in '{file}'".format(
                file=filename, user=self._user))
            self.sub_clever()
        else:
            print("Exporting {user}'s subreddits to {file}".format(
                file=filename, user=self._user))
            self.export_subs()

    def unsub(self, subreddit):
        '''
        Unsubscribes and prints to STDOUT
        '''
        self._r.subreddit(subreddit).unsubscribe()
        print("Unsubscribed from subreddit {sub}".format(sub=subreddit))

    def sub(self, subreddit):
        '''
        Try to subscribe to a given subreddit.
        '''
        self._r.subreddit(subreddit).subscribe()
        print("Subscribed to {sub}".format(sub=subreddit))

    def get_wanted_subs(self):
        '''
        Opens the list of subreddits we want to subscribe to
        from a json fille.
        '''
        fh = open(self._filename, 'r')
        subs = json.load(fh)
        fh.close()
        return list(set(subs))

    def sub_clever(self):
        '''
        Use the minimal number of API calls to subscribe / unsubscribe.
        '''
        wanted_subs = set(self.get_wanted_subs())
        current_subs = set(self.get_subs())
        for sub in wanted_subs - current_subs:
            if sub in wanted_subs:
                # Subscribe to wanted subs we're not already subbed to
                self.sub(sub)
        #for sub in current_subs - wanted_subs:
            # Unsub from everything remaining
            #self.unsub(sub)

    def get_user(self):
        '''
        Specifically returns the username from the Reddit object, not the one
        specified by the user / script. This is guaranteed to be correct in
        other words.
        '''
        return str(self._r.user.me())

    def export_subs(self):
        '''
        Saves the user's subreddits to file.
        '''
        fh = open(self._filename, 'w')
        subs = sorted(self.get_subs(), key=str.lower)
        json.dump(subs, fh, indent=2)
        fh.close()

    def get_subs(self):
        '''
        Returns a unique list of subreddits to which the user is subscribed.
        '''
        my_subs = set()
        for sub in self._r.user.subreddits(limit=None):
            my_subs.add(str(sub))
        return list(my_subs)


if __name__ == "__main__":
    args = parser.parse_args()

    # Boolean, True if --import / -i
    # If true then subscribe, if false then export to file.
    subscribe = getattr(args, 'import')

    r = Resub(subscribe,
              filename=getattr(args, 'file'),
              user=getattr(args, 'user'),
              )
