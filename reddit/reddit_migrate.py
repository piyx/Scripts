import os
import json

import praw
from dotenv import load_dotenv

# Make sure to populate the .env file with credentials
load_dotenv('.env')


CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USER_AGENT = os.getenv("USER_AGENT")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")


def get_subreddit_list() -> list[str]:
    '''Get list of subreddits joined by the user'''
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT,
        username=REDDIT_USERNAME,
        password=REDDIT_PASSWORD,
    )

    return [str(subreddit) for subreddit in reddit.user.subreddits(limit=None)]


def write_subreddits(subreddits: list[str]) -> None:
    '''Write list of subreddits to a json file'''
    with open("joined_subreddits.json", "w") as f:
        json.dump(subreddits, f)


def join_subreddits(subreddits: list[str]) -> None:
    '''Joins all the subreddits from the subreddits list'''
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT,
        username=REDDIT_USERNAME,
        password=REDDIT_PASSWORD,
    )

    # Subscribe/Join all the subreddits from the given list
    reddit.subreddit(subreddits[0]).subscribe(subreddits[1:])


def main():
    # Reading list of subreddits join_subreddits_json file
    joined_subreddits_file = "joined_subreddits.json"
    with open(joined_subreddits_file, "r") as f:
        subreddits = json.load(f)
    
    join_subreddits(subreddits)
    print("Successfully joined all subreddits!")


if __name__=="__main__":
    main()