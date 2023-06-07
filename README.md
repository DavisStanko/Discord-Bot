# Discord-Bot

My instance of this bot is hosted on a cheap VPS with a low bandwidth cap and as such it is only availible for private use. Feel free, to fork this program for your own bot instance.

## Usage

Commands are all prefixed with `!`. The bot will ignore any messages that do not start with this prefix. `!help` will list all available commands.

### Content Commands

`!content` is replied to with a list of all the available content commands. These commands are used to send media files to the discord server. For example, `!animal` will send a random cat picture or video.

### Game Commands

`!game` is replied to with a list of all the available game commands. These commands are used to play games with the bot. For example, `!trivia` will send a random trivia question and the bot will wait for a response. The bot will then reply with whether the answer was correct or not.

### Gambling Commands

`!gamble` is replied to with a list of all the available gambling commands. These commands are used to gamble with the bot. For example, `!roulette [red|black|green] [amount]` will wager the specified amount on the specified color. The bot will then reply with whether the wager was successful or not.

Users can create a gambling account with `!start`. This will create an account with a starting balance. The user can then use `!points` to check their balance.

### Utility

`!utility` is replied to with a list of all the available utility commands. These commands are used to perform various tasks. For example, `!weather [location] [info|now|hour (0-47)|day (0-7)]` will send weather information for the specified location and time. The bot will then reply with the requested information.

## License

This project is licensed under the [GPL-3.0](LICENSE.md)
GNU General Public License - see the [LICENSE.md](LICENSE.md) file for
details.
