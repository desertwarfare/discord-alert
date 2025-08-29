Discord Alert Monitor Script (Self Automation)
Author: desert.warfare

This is a script I made a while back, the story behind it is that I was part of a SWAT team in a roleplay game.
The idea behind it is whenever they needed SWAT ingame, they would tag us in a channel and ask us to hop in, however I would miss these tags because I don't check discord often.
Instead, this script would poll for any tags with keywords such as "requesting SWAT" and play a continous alarm sound and prompt me whether to confirm response and hop ingame.

TLDR: This script checks if you had been tagged by a specific role, or a certain keyword was sent over a specific channel and a 'special' alarm would sound off with a prompt to both launch game and send a message back.

This is one of my first Python scripts ever, so if it looks messy or not good, then I don't really care. As long as it worked for me, that was good enough until I received a warning from Discord.

Requirements:
- Python 3.8+
- Libraries: requests, pygame


WARNING: This script uses a user token, which is **against Discord's Terms of Service** for automation.
Using a user token for automation can result in your Discord account being permanently banned.
This script is intended for educational purposes only. **DO NOT** use it with your main Discord account. BETTER YET, use it with a bot or something.

For safe automation, consider using a **Discord bot** and the official [discord.py](https://discordpy.readthedocs.io/en/stable/) library.
