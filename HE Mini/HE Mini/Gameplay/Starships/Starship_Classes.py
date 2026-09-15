# Starship.py
import discord
from discord.ext import commands
from dataclasses import dataclass
from typing import Dict, Generic, Literal, Type, TypeVar


StarshipType = TypeVar("StarshipType", Literal["civilian"], Literal["military"])


@dataclass(frozen=True)
class ShieldAllocation:
    particle: tuple[int, ...]
    chetherite: tuple[int, ...]

    @property
    def total(self) -> int:
        return sum(self.particle) + sum(self.chetherite)

def _divide_evenly(value: int, count: int) -> tuple[int, ...]:
    """Divide an integer among shields without losing any hull points."""
    if count == 0:
        return ()
    whole, remainder = divmod(value, count)
    return tuple(whole + int(index < remainder) for index in range(count))


class StarshipClass(Generic[StarshipType]):
    """Base class for manually defined starship classes and subclasses."""

    starship_type: StarshipType
    hull: int = 0
    particle_shields: int = 0
    chetherite_shields: int = 0

    @classmethod
    def shield_allocation(cls) -> ShieldAllocation:
        if cls.hull < 0 or cls.particle_shields < 0 or cls.chetherite_shields < 0:
            raise ValueError("Hull and shield counts cannot be negative.")
        if cls.particle_shields + cls.chetherite_shields == 0:
            raise ValueError("A starship must have at least one shield.")

        chetherite_hull = cls.hull // 3 if cls.chetherite_shields else 0
        particle_hull = cls.hull - chetherite_hull
        return ShieldAllocation(
            particle=_divide_evenly(particle_hull, cls.particle_shields),
            chetherite=_divide_evenly(chetherite_hull, cls.chetherite_shields),
        )


# These are the civilian starships.
class Shuttle(StarshipClass):
    starship_type = "civilian"
    hull = 1000
    particle_shields = 1
    chetherite_shields = 0

class Transport(StarshipClass):
    starship_type = "civilian"
    hull = 2000
    particle_shields = 3
    chetherite_shields = 0

class LightFreighter(StarshipClass):
    starship_type = "civilian"
    hull = 4000
    particle_shields = 6
    chetherite_shields = 0

class BlockadeRunner(LightFreighter):
    starship_type = "military"
    hull = 4500
    particle_shields = 7
    chetherite_shields = 0

class MediumFreighter(StarshipClass):
    starship_type = "civilian"
    hull = 8000
    particle_shields = 12
    chetherite_shields = 1

class HeavyFreighter(StarshipClass):
    starship_type = "civilian"
    hull = 12000
    particle_shields = 17
    chetherite_shields = 1

class Barge(StarshipClass):
    starship_type = "civilian"
    hull = 20000
    particle_shields = 26
    chetherite_shields = 2

class JumpFreighter(Barge):
    starship_type = "civilian"
    hull = 32000
    particle_shields = 39
    chetherite_shields = 3

class IndustrialCommandShip(Barge):
    starship_type = "civilian"
    hull = 32000
    particle_shields = 39
    chetherite_shields = 3

# These are the military starship classes.

class Starfighter(StarshipClass):
    starship_type = "military"
    hull = 500
    particle_shields = 1
    chetherite_shields = 0

class Scrambler(Starfighter):
    starship_type = "military"
    hull = 500
    particle_shields = 1
    chetherite_shields = 0

class Recon(Starfighter):
    starship_type = "military"
    hull = 1000
    particle_shields = 1
    chetherite_shields = 0

class Gunship(StarshipClass):
    starship_type = "military"
    hull = 2000
    particle_shields = 3
    chetherite_shields = 0

class AssaultGunship(Gunship):
    starship_type = "military"
    hull = 2500
    particle_shields = 4
    chetherite_shields = 0

class InterdictorGunship(Gunship):
    starship_type = "military"
    hull = 2500
    particle_shields = 4
    chetherite_shields = 0

class Corvette(StarshipClass):
    starship_type = "military"
    hull = 4000
    particle_shields = 6
    chetherite_shields = 0

class AssaultCorvette(Corvette):
    starship_type = "military"
    hull = 4500
    particle_shields = 7
    chetherite_shields = 0

class StasisCorvette(Corvette):
    starship_type = "military"
    hull = 4500
    particle_shields = 7
    chetherite_shields = 0

class InterdictorCorvette(Corvette):
    starship_type = "military"
    hull = 4500
    particle_shields = 7
    chetherite_shields = 0

class LogisticsCorvette(Corvette):
    starship_type = "military"
    hull = 4500
    particle_shields = 7
    chetherite_shields = 0

class Frigate(StarshipClass):
    starship_type = "military"
    hull = 8000
    particle_shields = 12
    chetherite_shields = 1

class BlackOpsFrigate(Frigate):
    starship_type = "military"
    hull = 8500
    particle_shields = 12
    chetherite_shields = 1

class MissileFrigate(Frigate):
    starship_type = "military"
    hull = 8500
    particle_shields = 12
    chetherite_shields = 1

class AssaultFrigate(Frigate):
    starship_type = "military"
    hull = 8500
    particle_shields = 12
    chetherite_shields = 1

class Destroyer(StarshipClass):
    starship_type = "military"
    hull = 12000
    particle_shields = 17
    chetherite_shields = 1

class AssaultDestroyer(Destroyer):
    starship_type = "military"
    hull = 12500
    particle_shields = 17
    chetherite_shields = 1

class InterdictorDestroyer(Destroyer):
    starship_type = "military"
    hull = 12500
    particle_shields = 17
    chetherite_shields = 1

class Cruiser(StarshipClass):
    starship_type = "military"
    hull = 16000
    particle_shields = 21
    chetherite_shields = 2

class MissileCruiser(Cruiser):
    starship_type = "military"
    hull = 16500
    particle_shields = 22
    chetherite_shields = 2

class LogisticsCruiser(Cruiser):
    starship_type = "military"
    hull = 16500
    particle_shields = 22
    chetherite_shields = 2

class Battlecruiser(StarshipClass):
    starship_type = "military"
    hull = 20000
    particle_shields = 26
    chetherite_shields = 3

class Lancer(Battlecruiser):
    starship_type = "military"
    hull = 32000
    particle_shields = 39
    chetherite_shields = 3

STARSHIP_CLASSES: Dict[str, Type[StarshipClass]] = {
    "shuttle": Shuttle,
    "transport": Transport,
    "light_freighter": LightFreighter,
    "blockade_runner": BlockadeRunner,
    "medium_freighter": MediumFreighter,
    "heavy_freighter": HeavyFreighter,
    "barge": Barge,
    "jump_freighter": JumpFreighter,
    "industrial_command_ship": IndustrialCommandShip,
    "scrambler": Scrambler,
    "recon": Recon,
    "gunship": Gunship,
    "assault_gunship": AssaultGunship,
    "interdictor_gunship": InterdictorGunship,
    "corvette": Corvette,
    "assault_corvette": AssaultCorvette,
    "stasis_corvette": StasisCorvette,
    "interdictor_corvette": InterdictorCorvette,
    "logistics_corvette": LogisticsCorvette,
    "frigate": Frigate,
    "black_ops_frigate": BlackOpsFrigate,
    "missile_frigate": MissileFrigate,
    "assault_frigate": AssaultFrigate,
    "destroyer": Destroyer,
    "assault_destroyer": AssaultDestroyer,
    "interdictor_destroyer": InterdictorDestroyer,
    "cruiser": Cruiser,
    "missile_cruiser": MissileCruiser,
    "logistics_cruiser": LogisticsCruiser,
    "battlecruiser": Battlecruiser,
    "lancer": Lancer,
}


class Starship_Classes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot



async def setup(bot: commands.Bot):
    await bot.add_cog(Starship_Classes(bot))