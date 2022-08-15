from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from unit import BaseUnit


class Skill(ABC):
    _name: str
    _damage: float
    _need_stamina: float

    @abstractmethod
    def _skill_effect(self, *args):
        pass

    def use(self, unit, target) -> str:
        if unit.stamina >= self._need_stamina:
            self._skill_effect(target)
            unit._is_used_skill = True
            return f'{unit.name} использует {self._name} и наносит {self._damage} урона сопернику. '
        return f'{unit.name} попытался использовать {self._name}, но у него не хватило выносливости. '


class FuryPunch(Skill):
    _name = 'Свирепый пинок'
    _damage = 12
    _need_stamina = 8

    def _skill_effect(self, target):
        target.get_self_damage(self._damage)


class HardShot(Skill):
    _name = 'Мощный укол'
    _damage = 15
    _need_stamina = 5

    def _skill_effect(self, target):
        target.get_self_damage(self._damage)
