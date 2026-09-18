# Starship_Crafting.py
from __future__ import annotations

from collections import Counter
from copy import deepcopy
from typing import Any, Iterable

import discord
from discord.ext import commands

from .Starship_Classes import STARSHIP_CLASSES
from .Starship_Parts import StarshipPart


# Add one entry here for every hull that should be craftable. The values are
# parttype values from Starship_Parts.py, not individual part definitions.
# Any compatible part matching an optional parttype will be offered in the menu.
STARSHIP_RECIPES: dict[str, dict[str, list[str]]] = {
    "shuttle": {
        "required": ["Chassis", "Thruster", "Hyperdrive", "Navigation Computer", "Fuel Tank"],
        "optional": ["Hardpoint"],
    },
}

OPTIONAL_MASS_FRACTION = 13


def _part_classes(part_class: type[StarshipPart]) -> Iterable[type[StarshipPart]]:
    for child in part_class.__subclasses__():
        yield child
        yield from _part_classes(child)


def get_starship_parts() -> dict[str, StarshipPart]:
    """Build a catalog from the part definitions in Starship_Parts.py."""
    parts = {}
    for part_class in _part_classes(StarshipPart):
        part = StarshipPart(
            name=part_class.name,
            description=part_class.description,
            cost=part_class.cost,
            mass=part_class.mass,
            compatible_classes=deepcopy(part_class.compatible_classes),
            parttype=part_class.parttype,
            stats=deepcopy(part_class.stats),
        )
        if part.name:
            parts[part_class.__name__] = part
    return parts


def fleet_inventory_capacity(fleet: Any) -> int:
    """Return fleet inventory capacity: total ship cargo multiplied by four."""
    if not fleet:
        return 0
    ships = fleet.get("ships", fleet) if isinstance(fleet, dict) else fleet
    total_cargo = 0
    for ship in ships if isinstance(ships, list) else []:
        if isinstance(ship, str):
            ship_class = STARSHIP_CLASSES.get(ship)
            cargo = getattr(ship_class, "Cargo", 0)
            quantity = 1
        else:
            ship_class_name = ship.get("class", ship.get("starship_class", ""))
            ship_class = STARSHIP_CLASSES.get(ship_class_name)
            cargo = ship.get("cargo", getattr(ship_class, "Cargo", 0))
            quantity = ship.get("quantity", 1)
        total_cargo += int(cargo) * int(quantity)
    return total_cargo * 4


def combined_parts(station_storage: dict[str, int], fleet_inventory: dict[str, int]) -> Counter:
    """Return part counts available from both storage locations."""
    available = Counter()
    available.update({key: int(value) for key, value in station_storage.items()})
    available.update({key: int(value) for key, value in fleet_inventory.items()})
    return available


def _compatible(part: StarshipPart, class_name: str) -> bool:
    if not part.compatible_classes or any(isinstance(item, dict) for item in part.compatible_classes):
        return True
    return class_name.lower() in {str(item).lower() for item in part.compatible_classes}


def recipe_parts(class_name: str) -> tuple[list[str], list[str]]:
    recipe = STARSHIP_RECIPES.get(class_name, {})
    return recipe.get("required", []), recipe.get("optional", [])


def compatible_recipe_parts(
    class_name: str,
    parttypes: Iterable[str],
    catalog: dict[str, StarshipPart],
) -> list[str]:
    allowed_types = {parttype.lower() for parttype in parttypes}
    return [
        key
        for key, part in catalog.items()
        if part.parttype.lower() in allowed_types and _compatible(part, class_name)
    ]


def optional_hull_bonus(class_name: str, selected_parts: Iterable[str], catalog: dict[str, StarshipPart]) -> int:
    """Convert optional component mass into hull, capped at one thirteenth."""
    original_hull = STARSHIP_CLASSES[class_name].hull
    optional_mass = sum(catalog[key].mass for key in selected_parts)
    mass_bonus = optional_mass // OPTIONAL_MASS_FRACTION
    return min(mass_bonus, original_hull // OPTIONAL_MASS_FRACTION)


class CraftingView(discord.ui.View):
    def __init__(self, author_id: int, user_data: dict[str, Any]):
        super().__init__(timeout=300)
        self.author_id = author_id
        self.user_data = user_data
        self.catalog = get_starship_parts()
        self.selected_class: str | None = None
        self.selected_parts: list[str] = []
        self._build_class_selects()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("These crafting controls belong to another user.", ephemeral=True)
            return False
        return True

    def _build_class_selects(self):
        configured_classes = [key for key in STARSHIP_CLASSES if key in STARSHIP_RECIPES]
        civilian = [key for key in configured_classes if STARSHIP_CLASSES[key].starship_type == "civilian"]
        military = [key for key in configured_classes if STARSHIP_CLASSES[key].starship_type == "military"]
        for placeholder, options in (("Choose a civilian hull", civilian), ("Choose a military hull", military)):
            if options:
                select = discord.ui.Select(
                    placeholder=placeholder,
                    options=[discord.SelectOption(label=key.replace("_", " ").title(), value=key) for key in options],
                )
                select.callback = self.class_selected
                self.add_item(select)

    def _available(self) -> Counter:
        station = self.user_data.setdefault("station_storage", {})
        fleet = self.user_data.setdefault("fleet_inventory", {})
        return combined_parts(station, fleet)

    def embed(self) -> discord.Embed:
        title = "Craft Starship"
        description = "Choose a hull class with a configured recipe."
        if self.selected_class:
            required, optional = recipe_parts(self.selected_class)
            required_parts = compatible_recipe_parts(self.selected_class, required, self.catalog)
            missing = [
                parttype
                for parttype in required
                if not any(self._available()[key] > 0 for key in required_parts if self.catalog[key].parttype.lower() == parttype.lower())
            ]
            description = f"Hull: **{self.selected_class.replace('_', ' ').title()}**\nSelect every required part, then press Craft."
            if missing:
                description += "\nMissing: " + ", ".join(missing)
            if self.selected_parts:
                description += "\nSelected: " + ", ".join(self.catalog[key].name for key in self.selected_parts)
            description += f"\nOptional hull bonus: +{optional_hull_bonus(self.selected_class, [key for key in self.selected_parts if key in optional], self.catalog)}"
        fleet_capacity = fleet_inventory_capacity(self.user_data.get("fleets", []))
        return discord.Embed(title=title, description=description, color=discord.Color.blurple()).set_footer(
            text=f"Fleet inventory capacity: {fleet_capacity}"
        )

    async def class_selected(self, interaction: discord.Interaction):
        select = interaction.data["values"][0]
        self.selected_class = select
        self.selected_parts = []
        self.clear_items()
        required, optional = recipe_parts(select)
        options = []
        required_keys = compatible_recipe_parts(select, required, self.catalog)
        optional_keys = compatible_recipe_parts(select, optional, self.catalog)
        for key in required_keys + optional_keys:
            part = self.catalog[key]
            if self._available()[key] > 0:
                kind = "Required" if part.parttype.lower() in {value.lower() for value in required} else "Optional"
                options.append(discord.SelectOption(label=part.name, value=key, description=f"{kind} {part.parttype}"))
        if options:
            parts_select = discord.ui.Select(placeholder="Choose required parts", options=options, min_values=1, max_values=min(len(options), 25))
            parts_select.callback = self.parts_selected
            self.add_item(parts_select)
        craft_button = discord.ui.Button(label="Craft", style=discord.ButtonStyle.success)
        craft_button.callback = self.craft
        self.add_item(craft_button)
        await interaction.response.edit_message(embed=self.embed(), view=self)

    async def parts_selected(self, interaction: discord.Interaction):
        self.selected_parts = list(interaction.data["values"])
        await interaction.response.edit_message(embed=self.embed(), view=self)

    async def craft(self, interaction: discord.Interaction):
        if not self.selected_class or not self.selected_parts:
            await interaction.response.send_message("Choose a hull and at least one part first.", ephemeral=True)
            return
        required, optional = recipe_parts(self.selected_class)
        allowed_keys = set(compatible_recipe_parts(self.selected_class, required + optional, self.catalog))
        selected_types = {self.catalog[key].parttype.lower() for key in self.selected_parts}
        required_types = {parttype.lower() for parttype in required}
        if not required_types.issubset(selected_types) or not set(self.selected_parts).issubset(allowed_keys):
            await interaction.response.send_message("Select every part in the recipe before crafting.", ephemeral=True)
            return
        available = self._available()
        if any(available[key] < 1 for key in self.selected_parts):
            await interaction.response.send_message("One of those parts is no longer available.", ephemeral=True)
            return
        station = self.user_data.setdefault("station_storage", {})
        fleet = self.user_data.setdefault("fleet_inventory", {})
        for key in set(self.selected_parts):
            remaining = 1
            for inventory in (station, fleet):
                used = min(int(inventory.get(key, 0)), remaining)
                inventory[key] = int(inventory.get(key, 0)) - used
                remaining -= used
                if not remaining:
                    break
        optional_parts = [
            key for key in self.selected_parts
            if self.catalog[key].parttype.lower() in {parttype.lower() for parttype in optional}
        ]
        hull_bonus = optional_hull_bonus(self.selected_class, optional_parts, self.catalog)
        original_hull = STARSHIP_CLASSES[self.selected_class].hull
        self.user_data.setdefault("ships", []).append({
            "class": self.selected_class,
            "parts": self.selected_parts,
            "hull": original_hull + hull_bonus,
            "original_hull": original_hull,
        })
        save_data = getattr(interaction.client, "user_data", None)
        if save_data is not None:
            save_data.save()
        self.stop()
        await interaction.response.edit_message(embed=discord.Embed(title="Starship crafted", description=f"Your {self.selected_class.replace('_', ' ').title()} is ready. Hull: {original_hull + hull_bonus} (+{hull_bonus})."), view=None)


class Starship_Crafting(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def open_crafting_menu(
        self,
        destination: discord.abc.Messageable,
        author_id: int,
        station: Any,
    ) -> CraftingView | None:
        """Open crafting from a station drydock once stations are implemented."""
        has_drydock = (
            station.get("drydock", False)
            if isinstance(station, dict)
            else getattr(station, "drydock", False)
        )
        if not has_drydock:
            await destination.send("Starship crafting is only available from a station drydock.")
            return None

        save_data = getattr(self.bot, "user_data", None)
        if save_data is None:
            await destination.send("Player storage is not available yet.")
            return None
        view = CraftingView(author_id, save_data.get_user(author_id))
        view.message = await destination.send(embed=view.embed(), view=view)
        return view


async def setup(bot: commands.Bot):
    await bot.add_cog(Starship_Crafting(bot))