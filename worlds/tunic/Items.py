from pathlib import Path
from typing import Dict, List
from BaseClasses import ItemClassification, MultiWorld
import csv



class TunicItemData:
    name: str
    classification: ItemClassification
    quantity_in_item_pool: int
    region: str


class TunicItems:

    items: List[TunicItemData] = []
    items_lookup: Dict[str, TunicItemData] = {}

    def populate_items(self):
        item_file_path = (Path(__file__).parent / "data/Items.csv").resolve()
        with open(item_file_path) as item_file:
            csv_file = csv.reader(item_file)
            csv_file.__next__()
            for line in csv_file:
                item = TunicItemData()
                item.name = line[0]
                item.classification = getattr(ItemClassification, line[1])
                if item.classification == ItemClassification.filler:
                    filler_items.append(item.name)
                item.quantity_in_item_pool = int(line[4])
                self.items.append(item)
                self.items_lookup[item.name] = item

filler_items = []