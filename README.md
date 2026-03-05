# Discord Study Bot

A feature-rich Discord bot designed to help students manage study sessions and create interactive polls. Perfect for study groups, educational servers, and productivity tracking!

## Features

### Study Session Management
- **Start/End Sessions**: Track your study time with automatic break reminders
- **Session Status**: Check current session progress and duration
- **Break Reminders**: Automatic notifications after 30 minutes of studying
- **Duration Tracking**: Detailed session summaries with motivational achievements

### Interactive Polls
- **Create Polls**: Easy-to-use poll creation with multiple options
- **Real-time Results**: Check poll results anytime without ending the poll
- **Poll Management**: List active polls and end them when ready
- **Visual Feedback**: Emoji-based voting system with clear result display

### Social Features
- **Greeting Commands**: Friendly responses to common greetings
- **Rich Embeds**: Beautiful, colorful message formatting
- **User Permissions**: Creator-only controls for sessions and polls

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Discord.py library
- A Discord bot token

### Installation

1. **Clone or download the bot files**
2. **Install required dependencies:**
   ```bash
   pip install discord.py
   ```

3. **Set up your bot token:**
   - Create a file named `token.txt` in the same directory
   - Paste your Discord bot token inside (no quotes, just the token)

4. **Configure the bot:**
   - Open the Python file and find `CHANNEL_ID = 308289885767204864`
   - Replace with your desired channel ID where the bot will send notifications

5. **Run the bot:**
   ```bash
   python your_bot_file.py
   ```

## Commands

### Study Session Commands
| Command | Description | Usage |
|---------|-------------|-------|
| `!start` | Begin a new study session | `!start` |
| `!end` | End current study session | `!end` |
| `!status` | Check current session status | `!status` |

### Poll Commands
| Command | Description | Usage |
|---------|-------------|-------|
| `!create_poll` | Create a new poll | `!create_poll What's your favorite subject? \| Math \| Science \| History` |
| `!list_polls` | Show all active polls | `!list_polls` |
| `!poll_results` | Get results for a specific poll | `!poll_results 1234567890` |
| `!end_poll` | End a poll and show final results | `!end_poll 1234567890` |

### Greeting Commands
| Command | Description |
|---------|-------------|
| `!hello`, `!hi` | Friendly greetings |
| `!morning` | Good morning messages |
| `!evening` | Good evening messages |
| `!sup` | Casual greetings |
| `!bye` | Farewell messages |

### Utility Commands
| Command | Description |
|---------|-------------|
| `!help` | Show all available commands |

## 📋 Usage Examples

### Starting a Study Session
```
User: !start
Bot: 📚 Study Session Started!
     Session started at 14:30:25
     Student: John Doe
     Break Reminder: 30 minutes
```

### Creating a Poll
```
User: !create_poll What should we study next? | Mathematics | Physics | Chemistry | Biology
Bot: [Creates a poll with emoji reactions A, B, C, D]
```

### Checking Poll Results
```
User: !poll_results 1234567890
Bot: 📊 Poll Results
     What should we study next?
     
     🇦 Mathematics: 5 votes
     🇧 Physics: 3 votes
     🇨 Chemistry: 7 votes
     🇩 Biology: 2 votes
     
     🏆 Winner: Chemistry
```

### Ending a Study Session
```
User: !end
Bot: ✅ Study Session Completed!
     Great work, John Doe!
     Duration: 01:45:30
     Achievement: 🏆 Excellent focus! You studied for over 30 minutes!
```

## Configuration

### Customizable Settings
- **MAX_SESSION_TIME_MINUTES**: Change break reminder interval (default: 30 minutes)
- **CHANNEL_ID**: Set the channel for bot notifications
- **Greeting responses**: Customize bot personality in the `greeting_responses` dictionary

### Permission Requirements
The bot needs the following Discord permissions:
- Send Messages
- Read Message History
- Add Reactions
- Use External Emojis
- Embed Links

## Technical Details

### Built With
- **Discord.py**: Python Discord API wrapper
- **Python 3.8+**: Core programming language
- **Asyncio**: Asynchronous programming support

### Key Features Implementation
- **Dataclass Session Management**: Efficient session state tracking
- **Task Loops**: Automated break reminders
- **Rich Embeds**: Enhanced visual presentation
- **Error Handling**: Comprehensive error management
- **Permission Checks**: Secure command access control

## Troubleshooting

### Common Issues

**Bot doesn't respond to commands:**
- Check if the bot is online in your server
- Verify the bot has necessary permissions
- Ensure the command prefix is `!`

**Break reminders not working:**
- Confirm the CHANNEL_ID is correct
- Check bot permissions in the notification channel

**Poll commands failing:**
- Verify message IDs are correct (use Developer Mode in Discord)
- Ensure the poll hasn't been deleted

**Token errors:**
- Make sure `token.txt` exists and contains only your bot token
- Verify the token is valid and not expired

### Getting Help
1. Check the console output for error messages
2. Veri
