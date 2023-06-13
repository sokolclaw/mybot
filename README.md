# The first training bot

It has been tried out: 
1. Interaction with BotFather
2. Using external libraries and functions
3. Interacting with the bot not only through commands, but also through text
4. Working with external files
5. Keyboard creation
6. Code Refactoring
7. Action Logging

Works with Python-telegram-bot

## Preparing for work

Run in the console:
```
git clone https://github.com/sokolclaw/mybot
pip install -r requirments.txt
```
 
### Setting

Create a virtual environment
'''
python3 -m venv env
'''
Add the following data to the settings copy.py file:
```
API_KEY = "Put here your API KEY, from BotFather bot"
```

### Starting
To run the bot, run in the console:
```
python3 bot.py
```
