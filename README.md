# Discord-Bot

This Discord bot is no longer hosted or maintained. It was created as a fun project to learn Python but has since been replaced by a more robust bot written in JavaScript [DavisStanko/botterfly](https://github.com/DavisStanko/botterfly). This bot is still functional and can be used as a template for other Discord bots.

## Usage

Commands are all prefixed with `!`. The bot will ignore any messages that do not start with this prefix. `!help` will list all available commands.

### Content Commands

`!content` is replied to with a list of all the available content commands. These commands are used to send media files to the discord server. For example, `!animal` will send a random cat picture or video.

### Game Commands

`!games` is replied to with a list of all the available game commands. Users can create a game account with `!start`. This will create an account with a starting balance. The user can then use `!points` to check their balance. Games like `!trivia` and `!wordscramble` are give points to the user if they win. Users can also gamble their points with commands like `!roulette` and `!slots`.

### Utility Commands

`!utility` is replied to with a list of all the available utility commands. These commands are used to perform various tasks. For example, `!weather [location] [info|now|hour (0-47)|day (0-7)]` will send weather information for the specified location and time. The bot will then reply with the requested information.

### Scheduled Actions

`!schedule` is replied to with a list of all of the bot's scheduled actions. When configured the weather and news for the locations set by the admin will be sent to a channel set by the admin.

### Admin Commands

`!admin` is replied to with a list of all the available admin commands. These commands are used to perform various tasks exclusive to the server admin. These are used to configure scheduled commands.

## License

This project is licensed under the [GPL-3.0](LICENSE.md)
GNU General Public License - see the [LICENSE.md](LICENSE.md) file for
details.
