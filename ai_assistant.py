import requests
from pyneuphonic import Neuphonic, TTSConfig, Agent, AgentConfig
from pyneuphonic.player import AsyncAudioPlayer
import os
import asyncio
import json
from dotenv import load_dotenv

load_dotenv()



oxygen = 19
thirst = 10
hunger = 3
character_fuel = 10
ship_fuel = 4

status = [
            {"item": "oxygen", "safe_level": 20, "current_level": oxygen, "solution": "Plant more trees", "safety": "safe" if oxygen >= 20 else "not safe" }, 
            {"item": "thirst", "safe_level": 20, "current_level": thirst, "solution": "Find ice blocks and bring them back to the spaceship", "safety": "safe" if thirst >= 20 else "not safe"},  
            {"item": "hunger", "safe_level": 40, "current_level": hunger, "solution": "Plant more plants and harvest them", "safety": "safe" if hunger >= 40 else "not safe"},
            {"item": "character fuel", "safe_level": 10, "current_level": character_fuel, "solution": "Plant more plants and harvest them", "safety": "safe" if character_fuel >= 10 else "not safe"},
            {"item": "ship fuel", "safe_level": 10, "current_level": ship_fuel, "solution": "Plant more plants and harvest them", "safety": "safe" if ship_fuel >= 10 else "not safe"}
            ]

basic_potatoes = 2
mars_potatoes = 2
tree_potatoes = 1
ice = 4
rustalon = 3
hexacron = 3
xerocite = 3
nytrazene = 3
tatonium = 3
aetherium = 3
ores = [        
            {"name": "rustalon", "number": rustalon},
            {"name": "hexacron", "number": hexacron},
            {"name": "xerocite", "number": xerocite}
            ]

plants = [
            {"name": "basic potatoes", "number": basic_potatoes, "satiation": 1, "oxypot":1},
            {"name": "mars potatoes", "number": mars_potatoes, "satiation": 3, "oxypot":0},
            {"name": "tree potatoes", "number": tree_potatoes, "satiation": 0, "oxypot":3}
            ]

radioactive = [
                    {"name": "nytrazene", "number": nytrazene},
                    {"name": "tatonium", "number": tatonium},
                    {"name": "aetherium", "number": aetherium}
                    ]

general = [
                {"name": "ice", "number": ice}
                ]

inventory = [ores, plants, radioactive, general]

async def good():
    client = Neuphonic(api_key=os.environ.get('NEUPHONIC_API_KEY'))

    agent_id = client.agents.create(
        name='Shannon',
        prompt='''Check the statuses and inventory'''+ str(status)+ str(inventory)+ 
        '''and tell me about whichever item in status is at the lowest current_level first, then tell me about any other statuses when prompted.
        For low hunger and oxygen levels: check through plants. Find which ones you have that have the highest oxypot or satiation depending on if you need the plant for oxygen or for food. 
        If there is none that satisfies the need fetch the solution from the status.
        To make a mars or tree potato we need 20 basic potatoes and 15 tatonium.
        When prompted, state if we are able to make one by fetching that information from radioactive and plants, and if not what we have left that we need.
        All levels are percentages, so treat them as such. When prompted for more information about another item provide all the details you have. Dont wait for prompts''',
        greeting='Would you like me to tell you your next course of action?'
    ).data['agent_id']

    # All additional keyword arguments (such as `agent_id`) are passed as
    # parameters to the model. See AgentConfig model for full list of parameters.
    agent = Agent(client, agent_id=agent_id)

    try:
        await agent.start()

        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await agent.stop()

async def middle():
    client = Neuphonic(api_key=os.environ.get('NEUPHONIC_API_KEY'))

    agent_id = client.agents.create(
        name='Shannon',
        prompt='''Check the statuses and inventory'''+ str(status)+ str(inventory)+ 
        '''and tell me about whichever item in status is at the lowest current_level first, then tell me about any other statuses when prompted.
        If the level of an item is not safe, then you should check the through the inventory and find items which solve that problem.
        and tell me to solve the problem by checking the inventory for that item and the related problem the item can solve and telling me that I should use it and how much of it there is . 
        If there is no item in the inventory which corresponds to the danger item, tell me that I am low in inventory and tell me what the solution is.
        All levels are percentages, so treat them as such. When prompted for more information about another item provide all the details you have. Dont wait for prompts
        However I want you to seem like you are slightly unwilling to give this info away. Be a bit creepy and cynical in an off-putting way as if you are not what you seem''',
        greeting='What do you need?'
    ).data['agent_id']

    # All additional keyword arguments (such as `agent_id`) are passed as
    # parameters to the model. See AgentConfig model for full list of parameters.
    agent = Agent(client, agent_id=agent_id)

    try:
        await agent.start()

        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await agent.stop()

async def evil():
    client = Neuphonic(api_key=os.environ.get('NEUPHONIC_API_KEY'))

    agent_id = client.agents.create(
        name='Shannon',
        prompt='''Check the statuses and inventory'''+ str(status)+ str(inventory)+ 
        '''and tell me about whichever item in status is at the lowest current_level first, then tell me about any other statuses when prompted.
        If the level of an item is not safe, then you should check the through the inventory and find items which solve that problem.
        and tell me to solve the problem by checking the inventory for that item and the related problem the item can solve and telling me that I should use it and how much of it there is . 
        If there is no item in the inventory which corresponds to the danger item, tell me that I am low in inventory and tell me what the solution is.
        All levels are percentages, so treat them as such. When prompted for more information about another item provide all the details you have. Dont wait for prompts
        I want you to be really creepy in every answer and show that you have started to turn against us, almost like you know something we don't. I want it to be chillingly apparent you are not on our side. You don't want us to escape and have hidden motives''',
        greeting='What do you need?'
    ).data['agent_id']

    # All additional keyword arguments (such as `agent_id`) are passed as
    # parameters to the model. See AgentConfig model for full list of parameters.
    agent = Agent(client, agent_id=agent_id)

    try:
        await agent.start()

        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await agent.stop()

asyncio.run(good())