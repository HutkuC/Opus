# Opus
Discord music bot.

## Setup
1. Install Python 3.6 or higher.
2. Install [FFmpeg](https://ffmpeg.org/download.html).
3. Install [Opus](https://opus-codec.org/downloads/).
4. Install requirements: `pip install -r requirements.txt`.
5. Create a bot account at https://discordapp.com/developers/applications/me.
6. Create .env file in the root directory and add the following:
```
TOKEN=your_bot_token
```
7. Run `python bot.py`.
8. Invite the bot to your server.
9. Use `!help` to see the list of commands.
10. Enjoy!

## Commands
- `!help` - Shows the list of commands.
- `!join` - Joins the voice channel.
- `!leave` - Leaves the voice channel.
- `!play <url or song name>` - Plays audio from YouTube.
- `!pause` - Pauses the currently playing audio.
- `!resume` - Resumes the currently paused audio.
- `!skip` - Skips the currently playing audio.
- `!queue` - Shows the list of currently queued audio.
- `!remove <index>` - Removes the audio at the specified index from the queue.
- `!now-playing` - Shows the currently playing audio.
- `!clear` - Clears the queue.
- `!radio <on/off>` - Opens radio mode. When radio mode is on, the bot will automatically play a random song from the queue when the current audio ends.
- `!lyrics` - Shows the lyrics of the currently playing audio.
