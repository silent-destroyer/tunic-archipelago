import typing

from Options import Option, DefaultOnToggle, Toggle, StartInventoryPool, Choice


class SwordProgression(DefaultOnToggle):
    """Option to play with sword progression. Sword Progression adds four possible upgrades to find that will
    level up your sword in the order of Stick -> Sword -> Lvl 3 Sword -> Lvl 4 Sword."""
    display_name = "Sword Progression"


class StartWithSword(Toggle):
    """Option to start with a sword in the player's inventory."""
    display_name = "Start With Sword"


class KeysBehindBosses(Toggle):
    """Option to choose if the three hexagon keys are placed randomly or behind their respective boss fight"""
    display_name = "Keys Behind Bosses"


class AbilityShuffling(Toggle):
    """Choose whether to lock the usage of Prayer, Holy Cross*, and Ice Rod until the relevant poge of the manual is found.
        In Hexagon Quest, abilities are randomly unlocked at 5, 10, and 15 Gold Hexagons.
        *Certain Holy Cross usages are still allowed, such as free bombs, the seeking spell and other player-facing codes.
    """
    display_name = "Ability Shuffling"


class HexagonQuest(Toggle):
    """Choose whether to play the Hexagon Quest game mode. This mode shuffles 30 Golden Hexagons into the item pool and
    allows the game to be ended after collecting 20 of them."""
    display_name = "Hexagon Quest"


class FoolTraps(Choice):
    """Replaces low-to-medium value money rewards in the item pool with fool traps, which cause random negative
    effects to the player."""
    display_name = "Fool Traps"
    option_off = 0
    option_normal = 1
    option_double = 2
    option_onslaught = 3
    default = 1


tunic_options: typing.Dict[str, type(Option)] = {
    "sword_progression": SwordProgression,
    "start_with_sword": StartWithSword,
    "keys_behind_bosses": KeysBehindBosses,
    "ability_shuffling": AbilityShuffling,
    "hexagon_quest": HexagonQuest,
    "fool_traps": FoolTraps,
    "start_inventory_from_pool": StartInventoryPool
}
