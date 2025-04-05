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

if oxygen > 20:
    level = "safe"
status = [
            {"Item": "oxygen", "safe_level": 20, "current_level": oxygen, "solution": "Plant more trees", "safety": "safe" if oxygen >= 20 else "not safe" }, 
            {"Item": "water", "safe_level": 20, "current_level": thirst, "solution": "Find ice blocks and bring them back to the spaceship", "safety": "safe" if thirst >= 20 else "not safe"},  
            {"Item": "hunger", "safe_level": 40, "current_level": hunger, "solution": "Plant more plants and harvest them", "safety": "safe" if hunger >= 40 else "not safe"}
            ]

potatoes = 2
inventory = [
                {"item": "potatoes", "number": potatoes, "solves": "hunger, oxygen (by replanting)"}
                ]


async def main():
    client = Neuphonic(api_key=os.environ.get('NEUPHONIC_API_KEY'))

    agent_id = client.agents.create(
        name='Agent 1',
        prompt='''Check the statuses and inventory'''+ str(status)+ str(inventory)+ 
        '''and tell me about whichever item in status is at the lowest current_level first, then tell me about any other statuses when prompted.
        If the level of an item is not safe, then you should check the through the inventory and find items which solve that problem.
        and tell me to solve the problem by checking the inventory for that item and the related problem the item can solve and telling me that I should use it and how much of it there is . 
        If there is no item in the inventory which corresponds to the danger item, tell me that I am low in inventory and tell me what the solution is.
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

asyncio.run(main())