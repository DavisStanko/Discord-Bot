import asyncpraw
from asyncprawcore.exceptions import Forbidden
import random

def get_commands():
    # Define a dictionary of commands and their subreddits
    commands = {
        "meme": ["meme", "memes", "dankmemes", "AdviceAnimals"],
        "animal": ["aww", "eyebleach", "animalsbeingderps", "AnimalsBeingJerks"],
        "meirl": ["me_irl", "meirl", "2meirl4meirl"],
        "wholesome": ["wholesomememes", "MadeMeSmile", "HumansBeingBros"],
        "art": ["Art", "IDAP", "drawing"],
        "gaming": ["gaming", "pcgaming", "PS5"],
        "science": ["science", "space", "technology"],
        "nature": ["EarthPorn", "natureisfuckinglit", "NatureIsMetal"]
    }

    return commands

async def get_post(request, REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET):
    # Get the subreddits associated with the command
    subreddits = get_commands()[request]

    # Create a reddit instance
    reddit = asyncpraw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent="Discord Bot"
    )

    try:
        # Get a random subreddit and post
        subreddit = await reddit.subreddit(random.choice(subreddits))
        post = await subreddit.random()
        
        # Return title and url
        return f"{post.title}\n{post.url}", subreddit

    except Forbidden:
        return None, subreddit