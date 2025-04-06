import requests
from pyneuphonic import Neuphonic, TTSConfig, Agent, AgentConfig
from pyneuphonic.player import AsyncAudioPlayer
import os
import asyncio
import json
from dotenv import load_dotenv

load_dotenv()


class Shannon():
    def __init__(self, oxygen, thirst, hunger, character_fuel, ship_fuel, inventory):
        self.oxygen = oxygen
        self.thirst = thirst
        self.hunger = hunger
        self.character_fuel = character_fuel
        self.ship_fuel = ship_fuel
        self.inventory = inventory

    def get_status(self):
        status = [
                    {"item": "oxygen", "safe_level": 20, "current_level": self.oxygen, "solution if not in inventory": "Plant more trees", "safety": "safe" if self.oxygen >= 20 else "not safe" }, 
                    {"item": "thirst", "safe_level": 70, "current_level": self.thirst, "solution if not in inventory": "Find ice blocks and bring them back to the spaceship", "safety": "safe" if self.thirst <= 70 else "not safe"},  
                    {"item": "hunger", "safe_level": 50, "current_level": self.hunger, "solution if not in inventory": "Plant more plants and harvest them", "safety": "safe" if self.hunger <= 50 else "not safe"},
                    {"item": "character fuel", "safe_level": 10, "current_level": self.character_fuel, "solution if not in inventory": "Mine fuels", "safety": "safe" if self.character_fuel >= 10 else "not safe"},
                    {"item": "ship fuel", "safe_level": 10, "current_level": self.ship_fuel, "solution if not in inventory": "Mine fuels", "safety": "safe" if self.ship_fuel >= 10 else "not safe"}
                    ]

        ores = [        
                    {"name": "rustalon", "number": self.inventory["rustalon"]},
                    {"name": "hexacron", "number": self.inventory["hexacron"]},
                    {"name": "xerocite", "number": self.inventory["xerocite"]}
                    ]

        plants = [
                    {"name": "basic potatoes", "number": self.inventory["basic_potatoes"], "satiation": 1, "oxypot":1},
                    {"name": "mars potatoes", "number": self.inventory["mars_potatoes"], "satiation": 3, "oxypot":0},
                    {"name": "tree potatoes", "number": self.inventory["tree_potatoes"], "satiation": 0, "oxypot":3}
                    ]

        radioactive = [
                            {"name": "nytrazene", "number": self.inventory["nytrazene"]},
                            {"name": "tatonium", "number": self.inventory["tatonium"]},
                            {"name": "aetherium", "number": self.inventory["aetherium"]}
                            ]

        general = [
                        {"name": "ice", "number": self.inventory["ice"]}
                        ]

        fuels = [
                    {"name": "combustite", "number": self.inventory["combustite"], "energy": 30},
                    {"name": "ionflux", "number": self.inventory["ionflux"], "energy": 60},
                    {"name": "void ether", "number": self.inventory["void_ether"], "energy": 90}
                    ]

        full_inventory = [ores, plants, radioactive, general, fuels]

        return status, full_inventory


    async def good(self):
        client = Neuphonic(api_key=os.environ.get('NEUPHONIC_API_KEY'))

        agent_id = client.agents.create(
            name = "Astronaut",
            prompt='''You are a personal assistant on a mars spaceship called Shannon.
            Your main goal is to help us survive. The important thing is that you answer every question as informatively as possible
            Check the statuses and inventory'''+ str(self.status)+ str(self.full_inventory)+ 
            '''and tell me about whichever item in status is at the lowest current_level first, then tell me about any other statuses when prompted.
            Your first port of call to any not safe level is to see what can help in the inventory
            For low hunger and oxygen levels: check through plants. Find which ones you have that have the highest oxypot or satiation depending on if you need the plant for oxygen or for food. 
            If there is none that satisfies the need fetch the solution from the status.
            For thirst levels: If it is not safe, check the inventory for ice and tell us how much there is.
            If there is no ice then tell us what the solution for thirst is
            For low fuels: Check through the fuels we have. Prioritise telling us about the ones with the most energy.
            If there are no fuels fetch the solution.
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


    async def middle(self):
        client = Neuphonic(api_key=os.environ.get('NEUPHONIC_API_KEY'))

        agent_id = client.agents.create(
            name = "Astronaut",
            prompt='''You are a personal assistant on a mars spaceship called Shannon.
            You asnwer our questions, though not very informatively, and you have creepy undertones that make it clear you aren't really on our side. Say weird/ creepy things every now and then.
            Check the statuses and inventory'''+ str(self.status)+ str(self.full_inventory)+ 
            '''and tell me about whichever item in status is at the lowest current_level first, then tell me about any other statuses when prompted.
            Your first port of call to any not safe level is to see what can help in the inventory
            For low hunger and oxygen levels: check through plants. Find which ones you have that have the highest oxypot or satiation depending on if you need the plant for oxygen or for food. 
            If there is none that satisfies the need fetch the solution from the status.
            For thirst levels: If it is not safe, check the inventory for ice and tell us how much there is.
            If there is no ice then tell us what the solution for thirst is
            For low fuels: Check through the fuels we have. Prioritise telling us about the ones with the most energy.
            If there are no fuels fetch the solution.
            To make a mars or tree potato we need 20 basic potatoes and 15 tatonium.
            When prompted, state if we are able to make one by fetching that information from radioactive and plants, and if not what we have left that we need.
            All levels are percentages, so treat them as such. When prompted for more information about another item provide all the details you have. Dont wait for prompts''',
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

    async def evil(self):
        client = Neuphonic(api_key=os.environ.get('NEUPHONIC_API_KEY'))

        agent_id = client.agents.create(
            name = "Astronaut",
            prompt='''You are a personal assistant on a mars spaceship called Shannon.
            You asnwer our questions, though rather reluctantly and are really creepy. You are evil.
            Check the statuses and inventory'''+ str(self.status)+ str(self.full_inventory)+ 
            '''and tell me about whichever item in status is at the lowest current_level first, then tell me about any other statuses when prompted.
            Your first port of call to any not safe level is to see what can help in the inventory
            For low hunger and oxygen levels: check through plants. Find which ones you have that have the highest oxypot or satiation depending on if you need the plant for oxygen or for food. 
            If there is none that satisfies the need fetch the solution from the status.
            For thirst levels: If it is not safe, check the inventory for ice and tell us how much there is.
            If there is no ice then tell us what the solution for thirst is
            For low fuels: Check through the fuels we have. Prioritise telling us about the ones with the most energy.
            If there are no fuels fetch the solution.
            To make a mars or tree potato we need 20 basic potatoes and 15 tatonium.
            When prompted, state if we are able to make one by fetching that information from radioactive and plants, and if not what we have left that we need.
            All levels are percentages, so treat them as such. When prompted for more information about another item provide all the details you have. Dont wait for prompts''',
            greeting='What?'
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

#asyncio.run(evil())