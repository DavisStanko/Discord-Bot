import content

def get_help():
    reply = "I can help you with the following commands:\n" \
            "`!help` - Displays this help message.\n" \
            "`!content` - Lists content commands.\n" \
            "`!game` - Lists game commands.\n" \
            "`!gamble` - Lists gambling commands.\n" \
            "`!utility` - Lists utility commands.\n" \
            "`!schedule` - Explains scheduled events.\n" \
            
    return reply

def get_utility():
    reply = "I react to the following utility commands:\n" \
            "`!info` - Links to my GitHub page.\n" \
            "`!NdM` - Rolls N M-sided dice where N and M are positive integers.\n"
    return reply

def get_content():
    reply = f"I react to the following content commands by sending a random media file from the specified directory:\n{content.get_commands()}"
    return reply

def get_game():
    reply = f"I react to the following game commands:\n" \
            "`!trivia` - Starts a game of trivia.\n"
    return reply

def get_gamble():
    reply = f"I react to the following gambling commands:\n" \
            "`!start` - **Creates a new account** with 1000 points.\n" \
            "`!points` - Displays your current points.\n" \
            "`!income` - Gives you 100 points. Can only be used once every 30 minutes.\n" \
            "`!roulette [wager] [red|black|green]` - Plays a game of roulette.\n" \
            "`!slots [wager]` - Plays a game of slots.\n"
    return reply

def get_info():
    reply = f"I react to the following info commands:\n" \
            "`!info` - Links to my GitHub page.\n"
    return reply

def get_schedule():
    reply = f"Every 6 hours I will send the current weather and top 3 news articles for the locations specified by the server owner.\n" \
            "If you are the admin and would like to set your location, please contact the my owner."