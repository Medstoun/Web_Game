from dataclasses import dataclass
from typing import List, Optional
import random
import marshmallow_dataclass
import marshmallow
from constants import EQUIPMENT_FILE
import json


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    def get_damage_by_weapon(self) -> float:
        damage = random.uniform(self.min_damage, self.max_damage)
        return round(damage, 1)


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class EquipmentData:
    weapons: List[Weapon]
    armors: List[Armor]


class Equipment:
    def __init__(self):
        self._equipment = self._get_data()

    @staticmethod
    def _get_data():
        with open(EQUIPMENT_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
        try:
            equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError

    def get_weapon(self, weapon: str) -> Optional[Weapon]:
        for item in self._equipment.weapons:
            if weapon == item.name:
                return item
        return None

    def get_armor(self, armor: str) -> Optional[Armor]:
        for item in self._equipment.armors:
            if armor == item.name:
                return item
        return None

    def get_weapon_names(self) -> List[str]:
        return [i.name for i in self._equipment.weapons]

    def get_armor_names(self) -> List[str]:
        return [i.name for i in self._equipment.armors]
