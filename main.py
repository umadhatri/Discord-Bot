import os
import discord
import requests
import json
import random
from replit import db
from keep_alive import keep_alive



client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there!",
  "Don't give up!", 
  "We are all here for you!",
  "There is nothing in this world that you can't do!",
  "Strong belief moves mountains!",
  "You are a great person!"
]

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragements(index):
  encouragements = db["ecouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client)) 

@client.event
async def on_message(message):
    if message.author == client.user:
     return
  
    if message.content.startswith('$inspire'):
      quote = get_quote()
      await message.channel.send(quote)

    options = starter_encouragements

    if "encouragements" in db.keys():
      options = options + db["encouragements"]
  
    if any (word in message.content for word in sad_words):
      await message.channel.send(random.choice(options)) 





keep_alive()
token = os.environ['token']
client.run(os.getenv('token'))
