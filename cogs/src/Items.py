import math
import random
import re

class Items:

    def __init__(self, inventory):
        self.inventory = {}
        for item in inventory:
            quantity = item.split(" ")[0]
            name = " ".join(item.split(" ")[1:])
            self.inventory[name] = int(quantity)

    def get_percent(self, percentage=0.85):
        string_gift = ""
        for name, quantity in self.inventory.items():
            string_gift += f"{math.floor(int(quantity)*percentage)} {name}, "

        return string_gift[:-2]

    def get_little(self, percentage=0.08):
        string_gift = ""
        for name, quantity in self.inventory.items():
            if name == "gold" or random.uniform(0,1) > 0.8:
                string_gift += f"{math.ceil(int(quantity)*percentage)} {name}, "

        return string_gift[:-2]

def get_items_to_trade(content):
    quantity = re.findall("(?<=\*\*)([0-9,]+)(?=\*\*)", content)  # <-- inventory quantity
    inv_codes = re.findall("(?<=`)[a-z ]+(?=`)", content)  # <-- id inventory

    inventory = []

    for i in range(0, len(inv_codes)):
        inventory.append("{} {}".format(quantity[i].replace(",", ""), inv_codes[i]))

    return inventory

if __name__ == "__main__":
    test = """:gem: **14,257** · `gem` · Gem
            :moneybag: **638** · `gold` · Gold
            :tickets: **117** · `ticket` · Ticket
            :frame_photo: **3** · `spring crafts frame` · Frame: Spring Crafts
            :frame_photo: **3** · `springtide treats frame` · Frame: Springtide Treats
            :star: **2** · `excellent upgrade` · Card Upgrade (★★★☆)
            :star: **2** · `good upgrade` · Card Upgrade (★★☆☆)
            :frame_photo: **2** · `rustic springtide frame` · Frame: Rustic Springtide
            :adhesive_bandage: **1** · `bandage` · Bandage
            :star: **1** · `mint upgrade` · Card Upgrade (★★★★)"""
    
    items = Items(get_items_to_trade(test))
    #print(items.inventory)
    print(items.get_little())
    #print(items.get_percent()) """