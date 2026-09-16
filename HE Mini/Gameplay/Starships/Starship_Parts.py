# Starship_Parts.py
import discord
from discord.ext import commands
from dataclasses import dataclass, field
from typing import Any

from .Starship_Classes import STARSHIP_CLASSES


@dataclass
class StarshipPart:
    """Template describing parts that are used to craft a starship"""

    name: str = ""
    description: str = ""
    cost: int = 0
    mass: int = 0
    compatible_classes: list[str] = field(default_factory=list)
    parttype: str = ""
    stats: dict[str, Any] = field(default_factory=dict)

    def is_compatible(self, starship_class: str) -> bool:
        """Return whether this part is compatible with the given class."""
        return (
            not self.compatible_classes
            or starship_class in self.compatible_classes
        )


# Add completed StarshipPart definitions here as new parts are created.
STARSHIP_PARTS: dict[str, StarshipPart] = {
}
# Chassis Parts (this will be a long list)
class Shuttle_Chassis(StarshipPart):
    name = "Shuttle Chassis"
    description = "A basic chassis for a shuttle."
    cost = 1000
    mass = 330
    compatible_classes = ["Shuttle"]
    parttype = "Chassis"
    stats = {"hull": 1000, "particle_shields": 1, "chetherite_shields": 0}

class Transport_Chassis(StarshipPart):
    name = "Transport Chassis"
    description = "A basic chassis for a transport class starship"
    cost = 2000
    mass = 660
    compatible_classes = ["transport"]
    parttype = "Chassis"
    stats = {"hull": 2000, "particle_shields": 1, "chetherite_shields": 0}
# Thruster Parts, Different Ratios relating to Actual game
class Ion_Afterbuner_Hybrid_Thrusters(StarshipPart):
    name = "Hybrid Thrusters(IAFT)"
    description = "A proven method of propulsion"
    cost = 500
    mass = 200
    compatible_classes = ["shuttle", "transport", "light_freighter", "blockade_runner", "medium_freighter", "heavy_freighter", "barge", "jump_freighter", "industrial_command_ship"]
    stats = {"speed": 17.5, "Acceleration": 3, "Efficiency": 0.75}
# Hardpoint system in favor of altered combat considering Y axis is removed.
class Civilian_Hardpoint(StarshipPart):
    name = "Hardpoint C"
    description = "A Classic Hardpoint allowing for installation of Weaponry Or Mining Utilities."
    cost = 220
    mass = 130
    compatible_classes = ["shuttle", "transport", "light_freighter", "blockade_runner", "medium_freighter", "heavy_freighter", "barge", "jump_freighter", "industrial_command_ship"]

class Military_Hardpoint(StarshipPart):
    name = "Hardpoint M"
    description = "A Modified Hardpoint that can handle the recoil of sophisticated Weaponry and Light Mining Utilities"
    cost = 1350
    mass = 185
    compatible_classes = ["starfighter", "scrambler", "recon", "gunship", "assault_gunship", "interdictor_gunship", "corvette", "assault_corvette", "stasis_corvette", "interdictor_corvette", "logistics_corvette", "frigate", "black_ops_frigate", "missile_frigate", "assault_frigate", "destroyer", "assault_destroyer", "interdictor_destroyer", "cruiser", "missile_cruiser", "logistics_cruiser", "battlecruiser", "lancer"]
# Hyperdrives
class Hyperdrive_Tier_1(StarshipPart):
    name = "Hyperdrive Mk. i"
    description = "Hyper Subsystem: meant for local use."
    cost = 625
    mass = 115
    compatible_classes = [STARSHIP_CLASSES]
    stats = {"power": 30000, "chetherite_usage": 4}

class Hyperdrive_Tier_2(StarshipPart):
    name = "Hyperdrive Mk. ii"
    description = "Hyper Subsystem: meant for inter-planetary usage"
    cost = 850
    mass = 140
    compatible_classes = [STARSHIP_CLASSES]
    stats = {"power": 50000, "chetherite_usage": 4}

class Hyperdrive_Tier_3(StarshipPart):
    name = "Hyperdrive Mk. iii"
    description = "Hyper Subsystem: meant for cross-system usage"
    cost = 1120
    mass = 235
    compatible_classes = [STARSHIP_CLASSES]
    stats = {"power": 75000, "chetherite_usage": 6}

class Hyperdrive_Tier_4(StarshipPart):
    name = "Hyperdrive Mk. iv"
    description = "Hyper Subsystem: meant for cross-region usage"
    cost = 1950
    mass = 255
    compatible_classes = [STARSHIP_CLASSES]
    stats = {"power": 100000, "chetherite_usage": 12}
# Navigation Computer's
class Basic_Navigation_Computer(StarshipPart):
    name = "Basic Navigation Computer"
    description = "Navigation Computers provide a starship with the ability to jump to a specified coordinate without a Hyperspace Beacon."
    cost = 350
    mass = 60
    compatible_classes = [STARSHIP_CLASSES]
    stats = {"jump_range": 15000}

class Advanced_Navigation_Computer(StarshipPart):
    name = "Advanced Navigation Computer"
    description = "Navigation Computers provide a starship with the ability to jump to a specified coordinate without a Hyperspace Beacon."
    cost = 925
    mass = 245
    compatible_classes = [STARSHIP_CLASSES]
    stats = {"jump_range": 20000}
# Fuel Tank's
class Civilian_Fuel_Tank(StarshipPart):
    name = "Fuel Tank C"
    description = "Fuel Tank Fitted to Civilian Operations Precepts"
    cost = 1300
    mass = 130
    compatible_classes = [
        class_name
        for class_name, starship_class in STARSHIP_CLASSES.items()
        if starship_class.starship_type == "civilian"
    ]
    stats = {"capacity": 56}

class Military_Fuel_Tank(StarshipPart):
    name = "Fuel Tank M"
    description = "Fuel Tank Armored and Fitted to Battle Precepts"
    cost = 1725
    mass = 275
    compatible_classes = [
        class_name
        for class_name, starship_class in STARSHIP_CLASSES.items()
        if starship_class.starship_type == "military"
    ]
    stats = {"capacity": 139}
# Supercapital Cores
class Mini_Core(StarshipPart):
    name = "Mini SubReactor Core"
    description = "A Nuclear Reactor Core meant to Power Fighters of the Second Tech Tree."
    cost = 15000
    mass = 120
    compatible_classes = ["scrambler", "recon", "assault_gunship", "interdictor_gunship"]
    stats = {"Nofuelrequired"}

class Small_Core(StarshipPart):
    name = "Small SubReactor Core"
    description = "A Nuclear Reactor Core meant to power Small Starships"
    cost = 22650
    mass = 365
    compatible_classes = ["blockade_runner", "assault_corvette", "stasis_corvette", "interdictor_corvette", "logistics_corvette"]
    stats = {"Fuel": "Nitrogen"}

class Medium_Core(StarshipPart):
    name = "Medium SubReactor Core"
    description = "A Nuclear Reactor Core meant to power Starships of varying size"
    cost = 37255
    mass = 815
    compatible_classes = ["black_ops_frigate", "missile_frigate", "assault_frigate", "assault_destroyer", "interdictor_destroyer"]
    stats = {"Fuel": "Methane"}

class Large_Core(StarshipPart):
    name = "Large SubReactor Core"
    description = "A Nuclear Reactor Core meant to power Starships of the Largest Size"
    cost = 48120
    mass = 1200
    compatible_classes = ["missile_cruiser", "logistics_cruiser", "lancer", "industrial_command_ship",  "jump_freighter"]
    stats = {"Fuel": "Xenon"}

class Barge_Core(StarshipPart):
    name = "Barge SubReactor Core"
    description = "A Nuclear Reactor Core Fitted to the Exact Requirements of a Barge"
    cost = 37255
    mass = 815
    compatible_classes = ["barge"]
    stats = {"Fuel": "Hydrogen"}

class Cruiser_Core(StarshipPart):
    name = "Cruiser SubReactor Core"
    description = "A Nuclear Reactor Core Fitted to the Exact Requirements of a Cruiser"
    cost = 37255
    mass = 815
    compatible_classes = ["cruiser"]
    stats = {"Fuel": "Hydrogen"}

class BattleCruiser_Core(StarshipPart):
    name = "BattleCruiser SubReactor Core"
    description = "A Nuclear Reactor Core Fitted to the Exact Requirements of a BattleCruiser"
    cost = 37255
    mass = 815
    compatible_classes = ["battlecruiser"]
    stats = {"Fuel": "Hydrogen"}

class Starship_Parts(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

async def setup(bot: commands.Bot):
    await bot.add_cog(Starship_Parts(bot))
