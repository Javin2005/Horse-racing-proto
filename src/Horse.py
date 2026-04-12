import random


class Horse:
    def __init__(self, name):
        self.name = name


        self.speed = random.uniform(5.0,10.0)
        self.stamina = random.uniform(5.0,10.0)
        self.spirit = random.uniform(5.0,10.0)

        self.mud_affinity = random.uniform(0.8, 1.3)

        self.health = 100
        self.is_doped = False
        self.is_banned = False

    def race_score(self, track_condition):
        score = self.speed + (self.stamina * 0.5) + (self.spirit * 0.3)

        if track_condition == "Muddy":
            score *= self.mud_affinity

        if self.is_doped:
            score *= 1.25
        
        score += random.uniform(-1.0, 1.0)
        return score

    def __repr__(self):
        return f"{self.name} (spd:{self.speed:.1f} stm:{self.stamina:.1f})"
    


