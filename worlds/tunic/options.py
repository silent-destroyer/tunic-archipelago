from dataclasses import dataclass

from Options import DefaultOnToggle, Toggle, StartInventoryPool, Choice, Range, PerGameCommonOptions


class SwordProgression(DefaultOnToggle):
    """Adds four sword upgrades to the item pool that will progressively grant stronger melee weapons, including two new
    swords with increased range and attack power."""
    internal_name = "sword_progression"
    display_name = "Sword Progression"


class StartWithSword(Toggle):
    """Start with a sword in the player's inventory. Does not count towards Sword Progression."""
    internal_name = "start_with_sword"
    display_name = "Start With Sword"


class KeysBehindBosses(Toggle):
    """Places the three hexagon keys behind their respective boss fight in your world."""
    internal_name = "keys_behind_bosses"
    display_name = "Keys Behind Bosses"


class AbilityShuffling(Toggle):
    """Locks the usage of Prayer, Holy Cross*, and Ice Rod until the relevant pages of the manual have been found.
    If playing Hexagon Quest, abilities are instead randomly unlocked after obtaining 25%, 50%, and 75% of the required
    Hexagon goal amount.
    *Certain Holy Cross usages are still allowed, such as the free bomb codes, the seeking spell, and other
    player-facing codes.
    """
    internal_name = "ability_shuffling"
    display_name = "Ability Shuffling"


class FoolTraps(Choice):
    """Replaces low-to-medium value money rewards in the item pool with fool traps, which cause random negative
    effects to the player."""
    internal_name = "fool_traps"
    display_name = "Fool Traps"
    option_off = 0
    option_normal = 1
    option_double = 2
    option_onslaught = 3
    default = 1


class HexagonQuest(Toggle):
    """An alternate goal that shuffles Gold "Questagon" items into the item pool and allows the game to be completed
    after collecting the required number of them."""
    internal_name = "hexagon_quest"
    display_name = "Hexagon Quest"


class HexagonGoal(Range):
    """How many Gold Questagons are required to complete the game on Hexagon Quest."""
    internal_name = "hexagon_goal"
    display_name = "Gold Hexagons Required"
    range_start = 15
    range_end = 50
    default = 20


class ExtraHexagonPercentage(Range):
    """How many extra Gold Questagons are shuffled into the item pool, taken as a percentage of the goal amount."""
    internal_name = "extra_hexagon_percentage"
    display_name = "Percentage of Extra Gold Hexagons"
    range_start = 0
    range_end = 100
    default = 50


class EntranceRando(Toggle):
    """Randomize the connections between scenes.
    A small, very lost fox on a big adventure."""
    internal_name = "entrance_rando"
    display_name = "Entrance Rando"


class FixedShop(Toggle):
    """Forces the Windmill entrance to lead to a shop, and places only one other shop in the pool.
    Has no effect if Entrance Rando is not enabled."""
    internal_name = "fixed_shop"
    display_name = "ER Fixed Shop"


@dataclass
class TunicOptions(PerGameCommonOptions):
    sword_progression: SwordProgression
    start_with_sword: StartWithSword
    keys_behind_bosses: KeysBehindBosses
    ability_shuffling: AbilityShuffling
    entrance_rando: EntranceRando
    fixed_shop: FixedShop
    fool_traps: FoolTraps
    hexagon_quest: HexagonQuest
    hexagon_goal: HexagonGoal
    extra_hexagon_percentage: ExtraHexagonPercentage
    start_inventory_from_pool: StartInventoryPool
