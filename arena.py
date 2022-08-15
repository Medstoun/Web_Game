from constants import STAMINA_PER_ROUND
from unit import BaseUnit
from typing import Optional, Dict, Any


class BaseSingleton(type):
    _instances: Dict[Any, Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    stamina_per_round = STAMINA_PER_ROUND
    user: BaseUnit
    pc: BaseUnit
    battle_result: str = ''
    game_is_running = False

    def start_game(self, user: BaseUnit, pc: BaseUnit):
        self.game_is_running = True
        self.user = user
        self.pc = pc

    def next_turn(self) -> Optional[str]:
        pc_hit = self.pc.hit(self.user)
        if self.is_hp_null():
            self.game_over()
        else:
            self.stamina_regeneration()
        return pc_hit

    def stamina_regeneration(self):
        self.user.stamina = round(self.user.stamina + self.stamina_per_round * self.user.stamina_modify, 1)
        if self.user.stamina > self.user.unit_class.max_stamina:
            self.user.stamina = self.user.unit_class.max_stamina

        self.pc.stamina = round(self.pc.stamina + self.stamina_per_round * self.pc.stamina_modify, 1)
        if self.pc.stamina > self.pc.unit_class.max_stamina:
            self.pc.stamina = self.pc.unit_class.max_stamina

    def is_hp_null(self) -> Optional[str]:
        if self.user.hp > 0 and self.pc.hp > 0:
            return None
        elif self.user.hp > 0:
            battle_result = 'Игрок победил!'
        elif self.pc.hp > 0:
            battle_result = 'Игрок проиграл!'
        else:
            battle_result = 'Ничья!'
        self.battle_result = battle_result
        return battle_result

    def game_over(self) -> str:
        Arena._instances = {}
        self.game_is_running = False
        return self.battle_result

    def users_hit(self) -> Optional[str]:
        return self.user.hit(self.pc)

    def used_skill(self) -> Optional[str]:
        return self.user.get_skill_to_target(self.pc)
