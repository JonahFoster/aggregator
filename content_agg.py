import os
import praw
from abc import ABC, abstractmethod
from dotenv import load_dotenv

load_dotenv()

# Reddit Keys
REDDIT_SECRET = os.getenv('REDDIT_SECRET')
REDDIT_CLIENT = os.getenv('REDDIT_CLIENT')

class Source(ABC):
    # Connect to a source
    @abstractmethod
    def connect(self):
        pass
    # Fetch posts from source
    @abstractmethod
    def fetch(self):
        pass

# Connect to Reddits API
class RedditSource(Source):
    def connect(self):
        self.reddit_con = praw.Reddit(client_id = REDDIT_CLIENT, 
                                      client_secret = REDDIT_SECRET, 
                                      grant_type_access= 'client_credentials',
                                      user_agent= 'script/1.0')
        return self.reddit_con
    def fetch(self):
        pass

class GatorsReddit(RedditSource):
    def __init__(self) -> None:
        self.reddit_con = super().connect()
        self.new_submissions = []
    
    # Grab new submissions from FloridaGators subreddit
    def fetch(self, limit: int):
        self.new_submissions = self.reddit_con.subreddit('floridagators').new(limit=limit)

    def __repr__(self):
        urls = []
        for submission in self.new_submissions:
            urls.append(vars(submission)['url'])
        return '/n'.join(urls)

if __name__ == '__main__':
    reddit_new_gators = GatorsReddit()
    reddit_new_gators.fetch(limit = 1)
    print(reddit_new_gators)