import re
from bot import WppBot

# We set our bot by passing its name.
bot = WppBot('robozin')

# We start the bot by informing the group/person we are going to talk to.
bot.start('Junior')

# We set our greeting to join the group with two sentences in a list.
bot.greeting(['Bot: Oi sou o bot do Duarte!',
              'Bot: Use :: no início para falar comigo! Agora com chatgpt'])

# We are variable last message with nothing.
last_message = ''

# It will always be true so it will never go into our script.
while True:
    # We use the listening method that will set the text variable.
    new_message = bot.listen()
    
    # Now we validate whether the text sent in the group/person is the same as the last one read.
    # This validation is used to ensure that the bot does not respond to the same text over and over again.
    # We also validate whether the text has the command :: at the beginning so that it responds.
    if new_message != last_message and re.match(r'^::', new_message):
        # After passing validation, we set the text as the last text.
        last_message = new_message
        
        # We removed our bot activate command from the string.
        new_message = new_message.replace('::', '')
        
        # We try to leave the text in lowercase characters.
        new_message = new_message.lower()
        
        # We send it to the respond method that will respond to the group/person.
        bot.answer(new_message)
