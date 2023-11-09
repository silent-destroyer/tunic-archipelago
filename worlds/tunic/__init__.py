from typing import Dict, List, Any

from BaseClasses import Region, Location, Item, Tutorial, ItemClassification
from .Items import item_name_to_id, item_table, item_name_groups, fool_tiers, filler_items, slot_data_item_names
from .Locations import location_table, location_name_groups, location_name_to_id, hexagon_locations
from .Rules import set_location_rules, set_region_rules, randomize_ability_unlocks, gold_hexagon
from .ER_Rules import set_er_location_rules
from .Regions import tunic_regions
from .ER_Scripts import create_er_regions
from .Options import TunicOptions
from worlds.AutoWorld import WebWorld, World
from decimal import Decimal, ROUND_HALF_UP


class TunicWeb(WebWorld):
    tutorials = [
        Tutorial(
            tutorial_name="Multiworld Setup Guide",
            description="A guide to setting up the TUNIC Randomizer for Archipelago multiworld games.",
            language="English",
            file_name="setup_en.md",
            link="setup/en",
            authors=["SilentDestroyer"]
        )
    ]
    theme = "grassFlowers"
    game = "Tunic"


class TunicItem(Item):
    game: str = "Tunic"


class TunicLocation(Location):
    game: str = "Tunic"


class TunicWorld(World):
    """
    Explore a land filled with lost legends, ancient powers, and ferocious monsters in TUNIC, an isometric action game
    about a small fox on a big adventure. Stranded on a mysterious beach, armed with only your own curiosity, you will
    confront colossal beasts, collect strange and powerful items, and unravel long-lost secrets. Be brave, tiny fox!
    """
    game = "Tunic"
    web = TunicWeb()

    data_version = 2
    options: TunicOptions
    options_dataclass = TunicOptions
    item_name_groups = item_name_groups
    location_name_groups = location_name_groups

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id

    ability_unlocks: Dict[str, int]
    slot_data_items: List[TunicItem]
    tunic_portal_pairs: Dict[str, str]
    er_portal_hints: Dict[int, str]

    def generate_early(self) -> None:
        if self.options.start_with_sword and "Sword" not in self.options.start_inventory:
            self.options.start_inventory["Sword"] = 1

    def create_item(self, name: str) -> TunicItem:
        item_data = item_table[name]
        return TunicItem(name, item_data.classification, self.item_name_to_id[name], self.player)

    def create_items(self) -> None:
        keys_behind_bosses = self.options.keys_behind_bosses
        hexagon_quest = self.options.hexagon_quest
        sword_progression = self.options.sword_progression

        items: List[TunicItem] = []
        self.slot_data_items = []

        items_to_create: Dict[str, int] = {item: data.quantity_in_item_pool for item, data in item_table.items()}

        for money_fool in fool_tiers[self.options.fool_traps]:
            items_to_create["Fool Trap"] += items_to_create[money_fool]
            items_to_create[money_fool] = 0

        if sword_progression:
            items_to_create["Stick"] = 0
            items_to_create["Sword"] = 0
        else:
            items_to_create["Sword Upgrade"] = 0

        if keys_behind_bosses:
            for rgb_hexagon, location in hexagon_locations.items():
                hex_item = self.create_item(gold_hexagon if hexagon_quest else rgb_hexagon)
                self.multiworld.get_location(location, self.player).place_locked_item(hex_item)
                self.slot_data_items.append(hex_item)
                items_to_create[rgb_hexagon] = 0
            items_to_create[gold_hexagon] -= 3

        if hexagon_quest:
            # Calculate number of hexagons in item pool
            hexagon_goal = self.options.hexagon_goal
            extra_hexagons = self.options.extra_hexagon_percentage
            items_to_create[gold_hexagon] += int((Decimal(100 + extra_hexagons) / 100 * hexagon_goal).to_integral_value(rounding=ROUND_HALF_UP))

            # Replace pages and normal hexagons with filler
            for replaced_item in list(filter(lambda item: "Pages" in item or item in hexagon_locations, items_to_create)):
                items_to_create[self.get_filler_item_name()] += items_to_create[replaced_item]
                items_to_create[replaced_item] = 0

            # Filler items that are still in the item pool to swap out
            available_filler: List[str] = [filler for filler in items_to_create if items_to_create[filler] > 0 and
                                           item_table[filler].classification == ItemClassification.filler]

            # Remove filler to make room for extra hexagons
            for i in range(0, items_to_create[gold_hexagon]):
                fill = self.random.choice(available_filler)
                items_to_create[fill] -= 1
                if items_to_create[fill] == 0:
                    available_filler.remove(fill)

        for item, quantity in items_to_create.items():
            for i in range(0, quantity):
                tunic_item: TunicItem = self.create_item(item)
                if item in slot_data_item_names:
                    self.slot_data_items.append(tunic_item)
                items.append(tunic_item)

        self.multiworld.itempool += items

    def create_regions(self) -> None:
        self.tunic_portal_pairs = {}
        self.er_portal_hints = {}
        self.ability_unlocks = randomize_ability_unlocks(self.random, self.options)
        if self.options.entrance_rando:
            portal_pairs, portal_hints = create_er_regions(self)
            for portal1, portal2 in portal_pairs.items():
                self.tunic_portal_pairs[portal1.scene_destination()] = portal2.scene_destination()
            self.er_portal_hints = portal_hints

        else:
            for region_name in tunic_regions:
                region = Region(region_name, self.player, self.multiworld)
                self.multiworld.regions.append(region)

            for region_name, exits in tunic_regions.items():
                region = self.multiworld.get_region(region_name, self.player)
                region.add_exits(exits)

            for location_name, location_id in self.location_name_to_id.items():
                region = self.multiworld.get_region(location_table[location_name].region, self.player)
                location = TunicLocation(self.player, location_name, location_id, region)
                region.locations.append(location)

            victory_region = self.multiworld.get_region("Spirit Arena", self.player)
            victory_location = TunicLocation(self.player, "The Heir", None, victory_region)
            victory_location.place_locked_item(TunicItem("Victory", ItemClassification.progression, None, self.player))
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
            victory_region.locations.append(victory_location)

    def set_rules(self) -> None:
        if not self.options.entrance_rando:
            set_region_rules(self, self.options, self.ability_unlocks)
            set_location_rules(self, self.options, self.ability_unlocks)

    def get_filler_item_name(self) -> str:
        return self.random.choice(filler_items)

    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
        if self.options.entrance_rando:
            hint_data[self.player] = self.er_portal_hints

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data: Dict[str, Any] = {
            "seed": self.random.randint(0, 2147483647),
            "start_with_sword": self.options.start_with_sword,
            "keys_behind_bosses": self.options.keys_behind_bosses,
            "sword_progression": self.options.sword_progression,
            "ability_shuffling": self.options.ability_shuffling,
            "hexagon_quest": self.options.hexagon_quest,
            "fool_traps": self.options.fool_traps,
            "entrance_rando": self.options.entrance_rando,
            "Hexagon Quest Prayer": self.ability_unlocks["Pages 24-25 (Prayer)"],
            "Hexagon Quest Holy Cross": self.ability_unlocks["Pages 42-43 (Holy Cross)"],
            "Hexagon Quest Ice Rod": self.ability_unlocks["Pages 52-53 (Ice Rod)"],
            "Hexagon Quest Goal": self.options.hexagon_goal,
            "Entrance Rando": self.tunic_portal_pairs
        }

        for tunic_item in filter(lambda item: item.location is not None, self.slot_data_items):
            if tunic_item.name not in slot_data:
                slot_data[tunic_item.name] = []
            if tunic_item.name == gold_hexagon and len(slot_data[gold_hexagon]) >= 6:
                continue
            slot_data[tunic_item.name].extend([tunic_item.location.name, tunic_item.location.player])

        for start_item in self.options.start_inventory_from_pool:
            if start_item in slot_data_item_names:
                if start_item not in slot_data:
                    slot_data[start_item] = []
                for i in range(0, self.options.start_inventory_from_pool[start_item]):
                    slot_data[start_item].extend(["Your Pocket", self.player])

        return slot_data
