from __future__ import annotations

from abc import ABC, abstractmethod
from classes import UnitClass
from equipment import Weapon, Armor
from constants import CHANCE_TO_EFFECT_SKILL
from typing import Optional, Any
import random
import pymorphy2


class BaseUnit(ABC):
    def __init__(self, name: str, unit_class: UnitClass):
        self._name = name
        self._unit_class = unit_class
        self._hp = unit_class.max_health
        self._stamina = unit_class.max_stamina
        self._stamina_modify = unit_class.stamina
        self._weapon: Weapon
        self._armor: Armor
        self._is_used_skill = False

    def equip_weapon(self, weapon: Weapon):
        self._weapon = weapon

    def equip_armor(self, armor: Armor):
        self._armor = armor

    def _count_damage(self, enemy: BaseUnit) -> float:
        damage = self._weapon.get_damage_by_weapon() * self._unit_class.attack
        self._stamina = round(self._stamina - self._weapon.stamina_per_hit, 1)
        if self._stamina < 0:
            self._stamina = 0

        if enemy._stamina >= enemy._armor.stamina_per_turn:
            defence = enemy._armor.defence * enemy._unit_class.armor
            enemy._stamina = round(enemy._stamina - enemy._armor.stamina_per_turn, 1)
        else:
            defence = 0

        total_damage = round(damage - defence, 1)
        if total_damage > 0:
            enemy.get_self_damage(total_damage)
        else:
            total_damage = 0

        return total_damage

    def get_self_damage(self, damage: float):
        self._hp = round(self._hp - damage, 1)
        if self._hp < 0:
            self._hp = 0

    def get_skill_to_target(self, target: BaseUnit) -> Optional[str]:
        if self._is_used_skill:
            return None
        return self._unit_class.skill.use(unit=self, target=target)

    @abstractmethod
    def hit(self, enemy: BaseUnit) -> Optional[str]:
        pass

    def _strike(self, enemy: BaseUnit) -> str:
        if self._stamina >= self._weapon.stamina_per_hit:
            damage = self._count_damage(enemy)
            if damage != 0:
                return f'{self._name}, используя {self._get_accusative(self._weapon.name)}, пробивает' \
                       f' {self._get_accusative(enemy._armor.name)} соперника и наносит {damage} урона. '
            return f'{self._name}, используя {self._get_accusative(self._weapon.name)}, наносит удар, ' \
                   f'но {enemy._armor.name} соперника его останавливает. '
        return f'{self._name} попытался использовать {self._get_accusative(self._weapon.name)},' \
               f' но у него не хватило выносливости. '

    @staticmethod
    def _get_accusative(word: str) -> str:
        morph = pymorphy2.MorphAnalyzer()
        result = [morph.parse(elem)[0].inflect({'accs'}).word for elem in word.split()]
        return ' '.join(result)

    @property
    def name(self) -> str:
        return self._name

    @property
    def unit_class(self) -> UnitClass:
        return self._unit_class

    @property
    def hp(self) -> float:
        return self._hp

    @property
    def stamina(self) -> float:
        return self._stamina

    @stamina.setter
    def stamina(self, stamina):
        self._stamina = stamina

    @property
    def weapon(self) -> Weapon:
        return self._weapon

    @property
    def armor(self) -> Armor:
        return self._armor

    @property
    def stamina_modify(self) -> float:
        return self._stamina_modify


class UserUnit(BaseUnit):
    def hit(self, enemy: BaseUnit) -> Optional[str]:
        return self._strike(enemy)


class PC_Unit(BaseUnit):
    def hit(self, enemy: BaseUnit) -> Optional[str]:
        if not self._is_used_skill and random.random() <= CHANCE_TO_EFFECT_SKILL:
            return self.get_skill_to_target(enemy)

        return self._strike(enemy)
