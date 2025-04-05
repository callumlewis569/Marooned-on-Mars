import requests
from pyneuphonic import Neuphonic, TTSConfig, Agent, AgentConfig
from pyneuphonic.player import AsyncAudioPlayer
import os
import asyncio
import json
from dotenv import load_dotenv

load_dotenv()

oxygen = 19
water = 10
food = 50
status = [{"Item": "Oxygen", "safe_level": 20, "current_level": oxygen, "solution":"Plant more trees"}, {"Item": "water", "safe_level": 20, "current_level": water, "solution":"Find ice blocks and bring them back to the spaceship"},  {"Item": "food", "safe_level": 40, "current_level": food, "solution":"Plant more plants and harvest them"}]


async def main():
    client = Neuphonic(api_key=os.environ.get('NEUPHONIC_API_KEY'))

    agent_id = client.agents.create(
        name='Agent 1',
        prompt='Check the statuses'+ str(status)+ 'and tell me what the best course of action is if the current level is below the good level and only tell me about whichever item is at the lowest level. All levels are percentages, so treat them as such. When prompted for more information about another item provide all the details you have. Dont wait for prompts',
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