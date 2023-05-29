# Discord-Bot

This bot was made for educational purposes and has no theme. My instance of this bot is hosted on a cheap VPS with a low bandwidth cap and as such it is not available for public use. Feel free however, to fork this program for your own bot instance.

## Usage

This bots list of commands changes often. To see a complete list, send !help in a channel the bot has permission to respond in.

## Hosting

It is best to host this bot on a server. It can technically be done on your personal computer as well, just be sure not to turn it off. 

### Create a discord bot

I used this [guide](https://www.howtogeek.com/744801/how-to-add-a-bot-to-discord/) to create mine but opted to replace the word "guild" with "server" whenever is arose.  This guide should cover everything relevant to getting your bot connected to a discord server.

### Fork and change my program for your use

0. Please familiarize yourself with the terms of the [GPL-3.0](LICENSE.md) GNU General Public License before forking this project.
1. Put your discord bot's token in the .env file.
2. Put the server name(s) in the .env file.
    - The above guide should help with this.
3. Add your own files for the bots functions.
    - (eg. The bot's !meme function grabs and sends a random file from the meme folder. There is no meme folder by default, you will need to create this).
    - Make sure to follow the functions expected naming conventions. As of this documents writing, the meme function expects files to be numbered in ascending order (1, 2, 3) and only works on `.gif` `.mp4` and `.png` files.
    - Try to keep the files small. Discord requires you to have nitro to send large files and it may force users to download the files for viewing instead of having it embedded even if the files successfully sends.

### Get the files onto the server

I used **rsync** to send the files from my personal computer to the server. You may run into issues if either one of these computers are running windows. While Git Clone technically should work, I avoid it since my private files are not stored in this repository (eg. secrets, attachments, etc).

### Run the the main.py file on your server

I use the following command for this on my server but **you will probably need to modify it for your use**:
 `cd /home/discordbot && nohup python3 main.py &`
This command changes my directory to where I store the program and then runs the program in the background. To kill the program I use `pkill -f main.py`. **Be sure that there is no other main.py file running in the background** to avoid accidents. You will need to use a more specific command if you are running multiple main.py files.

## License

This project is licensed under the [GPL-3.0](LICENSE.md)
GNU General Public License - see the [LICENSE.md](LICENSE.md) file for
details.
