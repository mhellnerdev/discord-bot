import os
import requests
import json
import random
import logging

import discord

import boto3
from botocore.exceptions import ClientError

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
AWS_REGION=os.getenv('AWS_REGION')

# instantiate client
client = discord.Client()

sns_client = boto3.client('sns', region_name=AWS_REGION)

# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')


# helper function for storing random quote uri
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

# function to publish message to AWS sns topic
def publish_message(topic_arn, message, subject):
  """
  Publishes a message to a topic.
  """
  try:

    response = sns_client.publish(
      TopicArn=topic_arn,
      Message=message,
      Subject=subject
    )['MessageId']
    
  except ClientError:
    logger.exception(f'Could not publish to this topic.')
    raise
  else:
    return response


# print logged in message to console when bot is connected
@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))


# watch for ! to execute sending message to discord channel and publish to sns topic to send sms
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('!inspire'):
    quote = get_quote()
    await message.channel.send(quote)
    topic_arn = os.getenv('TOPIC_ARN')
    message = quote
    subject = 'subject'
    logger.info(f'Publishing message to topic - {topic_arn}...')
    message_id = publish_message(topic_arn, message, subject)
    logger.info(
      f'Message published to topic - {topic_arn} with message Id - {message_id}.'
    )
    print(quote)
 

#run client/bot passing in the discord token  
client.run(TOKEN)





