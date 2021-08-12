####################################################################
#																																	 #
#      Created by Steeve Johan Otoka Eyota and Davy Okemba				 #
#    Copyright © 2021 Steeve Johan Otoka Eyota and Davy Okemba		 #
#																																	 #
#												Weather Egg																 #
####################################################################

import discord
import requests
import json
import os

command_prefix = 'w:'
api_key = os.environ['API_KEY']
client = discord.Client()

##### KEY DICTIONNARY #####
key_features = {
	'temp' : 'Temperature',
	'feels_like' : 'Feels Likes',
	'temp_min' : 'Minimum Temperature',
	'temp_max' : 'Maximum Temperature',
	'humidity' : 'Humidity'
}

######################### HELPING FUNCTIONS ##############################
##### PARSING DATA #####
def parse_data(data):
	data = data['main']
	del data['pressure']
	return data

##### FORMATING MESSAGE #####
def weather_message(data, city_name):
	city_name = city_name.title()
	message = discord.Embed(
		title=f'{city_name} Weather', 
		description=f'Weather data for {city_name}.',
		color=0x0080FF  #Blue color
	) 
	for key in data:
		message.add_field(name=key_features[key], value=str(data[key]), inline=False)
	return message

######################### END OF HELPING FUNCTIONS ##############################

@client.event
async def on_ready():
		await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='One Piece'))
		print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	if message.author == client.user:
		return

######################### FUNCTIONALITIES ##############################
  ##### DISPLAYING WEATHER INFORMATION OF A GIVEN CITY #####
	if message.content.startswith(command_prefix):
			city_name = message.content.replace(command_prefix, '')
			if len(city_name) > 0:
					request = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
					data = json.loads(requests.get(request).content)
					data = parse_data(data)
					await message.channel.send(embed=weather_message(data, city_name))

	if message.content.startswith('{0}hello'.format(command_prefix)):
			await message.channel.send('Hello!')

client.run(os.getenv('TOKEN'))