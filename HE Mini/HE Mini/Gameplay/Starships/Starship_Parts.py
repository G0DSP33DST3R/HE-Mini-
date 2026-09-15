# Starship_Parts.py
import discord
from discord.ext import commands
from dataclasses import dataclass, field
from typing import Any

from .Starship_Classes import STARSHIP_CLASSES


@dataclass
class StarshipPart:
    """Template describing a part that can be installed on a starship."""

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
    compatible_classes = ["Transport"]
    parttype = "Chassis"
    stats = {"hull": 2000, "particle_shields": 1, "chetherite_shields": 0}

class Ion_Afterbuner_Hybrid_Thrusters(StarshipPart):
    name = "Hybrid Thrusters(IAFT)"
    description = "A proven method of propulsion"
    cost = 500
    mass = 200
    compatible_classes = ["Shuttle","Transport", "LightFreighter", "MediumFreighter", "HeavyFreighter", "Barge"]
    stats = {"speed": 100, "maneuverability": 50}

class Starship_Parts(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

async def setup(bot: commands.Bot):
    await bot.add_cog(Starship_Parts(bot))