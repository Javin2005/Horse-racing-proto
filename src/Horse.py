import random


class Horse:
    def __init__(self, name):
        self.name = name

        self.age = age or random.randint(2,4)


        self.speed = round(random.uniform(4.0,9.0),2)
        self.stamina = round(random.uniform(4.0,9.0),2)
        self.acceleration = round(random.uniform(3.0,9.0),2)

        self.weight = round(rando.uniform(450,600),1)

        self.experience = 0

        #Multplayer 1: Neutral, >1 positiv, <1 negativ
        self.mud_affinity = round(random.uniform(0.7, 1.2), 2)
        self.cornering = round(random.uniform(0.8, 1.2), 2)


        self.surface_pref = random.choice(["Grass", "Dirt", "Syntheic"])
        self.distance_pref = random.choice(["Sprinter", "Middle", "Stayer"])

        self.gate_start = round(random.uniform(0.7, 1.3), 2)

        #gömda stats som man ska räkna ut över tid.
        self._potential = round(ranadom.uniform(6.0,10.0), 2)
        self._learning_rate = round(random.uniform(0.05,0.25), 2)
        self._injury_proneness = round(random.uniform(0.02, 0.20), 2)
        self._doping_sensitivity = round(random.uniform(0.5, 1.8), 2)
        self._longevity = round(random.uniform(0.5, 1.0), 2)


        self.temperament = round(random.uniform(1.0, 3.0), 2)
        self.grit = round(random.uniform(0.8, 1.4), 2)
        self.focus = round(random.uniform(0.5, 1.0), 2)
        self.social_pref = random.choice(["Front-runner", "Closer", "Neutral"])


        self.fitness = round(random.uniform(60.0, 90.0), 1)
        self.fatigue = 0.0 
        self.morale = 75.0
        self.drug_level = 0.0 

        #status på hästen
        self.health = 100      
        self.is_doped = False
        self.is_banned = False
        self.is_injured = False
        self.races_run = 0
        self.career_wins = 0


    def calculate_race_score(self, track: str, surface: str, distance_m: int, position_in_field: int = 5) -> float:

        if self.is_banned or self.is_injured:
            return 0.0
        

        base = (
            self.speed * 0.40 +
            self.stamina * 0.30 +
            self.acceleration * 0.20 +
            (self.fitness / 100) * 10
        )
        
        if track == "Muddy":
            weight_penalty = (self.weight - 500) * 0.005
            base *= self.mud_affinity
            base -= weight_penalty
        
        if surface == self.surface_pref:
            base *= 1.10

        elif surface != self.surface_pref:
            base *= 0.95
        
        distance_modifier = self._distance_modifier(distance_m)
        base *= distance_modifier

        base += self.gate_start * 0.5
        base *= self.cornering

        temperament_drain = (self.temperament - 1.0) * 0.3
        base -= temperament_drain

        if self.social_pref == "Front-runner" and position_in_field <= 2:
            base *= 1.08

        elif self.social_pref == "Closer" and position_in_field > 4:
            base *= 1.10
        
        if self.fatigue > 50:
            fatigue_penalty = (self.fatigue - 50) * 0.02
            base -= fatigue_penalty
        
        morale_modifier = (self.morale / 75.0)
        base *= morale_modifier

        if self.is_doped:
            boost = 1.20 * self._doping_sensitivity
            base *= boost
            
            self.focus = max(0.1, self.focus - 0.15)
        

        experience_bonus = min(self.experience * 0.02, 1.0)
        base += experience_bonus

        base += random.uniform(-1.5, 1.5)

        return round(base, 3)


    def _distance_modifier(self, distance_m: int) -> float:

        if self.distance_pref == "Sprinter":
            if distance_m <= 1600:
                return 1.15   
            elif distance_m <= 2000:
                return 1.00
            else:
                return 0.85

        elif self.distance_pref == "Stayer":
            if distance_m >= 2200:
                return 1.15
            elif distance_m >= 1800:
                return 1.00
            else:
                return 0.88
        
        else:
            return 1.00
    
    def check_gait_break(self) -> bool:

        break_chance = 1 - self.focus
        return random.random() < break_chance
    
    def apply_post_race_effects(self, finished_position: int, field_size: int, was_doped: bool):

        self.races_run += 1
        self.experience = min(self.experience + 1, 20)

        self.fatigue = min(100, self.fatigue + random.uniform(10, 20))

        if finished_position == 1:
            self.career_wins += 1
            self.morale = min(100, self.morale + 15)
        elif finished_position <= field_size // 2:
            self.morale = min(100, self.morale + 5)   
        else:
            self.morale = max(0, self.morale - 8)

        self._apply_training_gain()

        if random.random() < self._injury_proneness:
            self.is_injured = True
            self.health = max(0, self.health - random.randint(10, 30))
            print(f"  !! {self.name} pulled up lame after the race.")

        if was_doped:
            self.drug_level = min(100, self.drug_level + 30 * self._doping_sensitivity)
        else:
            self.drug_level = max(0, self.drug_level - 15)

        if self.age > 7:
            decline = random.uniform(0, 0.1) / self._longevity
            self.speed   = max(1.0, self.speed - decline)
            self.stamina = max(1.0, self.stamina - decline)

        self.age_up_if_birthday()

    def _apply_training_gain(self):

        gain = self._learning_rate * random.uniform(0.5, 1.5)

        if self.speed < self._potential:
            self.speed = round(min(self._potential, self.speed + gain * 0.5), 2)
        if self.stamina < self._potential:
            self.stamina = round(min(self._potential, self.stamina + gain * 0.3), 2)

    def rest(self, weeks: int = 1):
        recovery = weeks * random.uniform(15, 25)
        self.fatigue = max(0, self.fatigue - recovery)
        self.fitness = min(100, self.fitness + weeks * 3)

    def age_up_if_birthday(self):
        self.age += 1
        if 4 <= self.age <= 7:
            self.speed = round(min(self._potential, self.speed + 0.2), 2)
            self.stamina = round(min(self._potential, self.stamina + 0.2), 2)
        
    def trainer_report(self, trainer_level: str = "basic") -> str:

        if trainer_level == "basic":
            potential_hint = "a lot of room to grow" if self._potential > 8 else \
                            "moderate potential" if self._potential > 6.5 else \
                            "probably close to their peak"
            injury_hint = "seems fragile might not be able to do much work" if self._injury_proneness > 0.12 else \
                            "robust constitution, handles hard racing well"
            
            return (
                f"--- Trainer's notes on {self.name} ---\n"
                f"  This horse has {potential_hint}.\n"
                f"  {injury_hint}\n"
                f"  Prefers {self.distance_pref.lower()} distances on {self.surface_pref.lower()}.\n"
                f"  {'Hates the rain.' if self.mud_affinity < 0.9 else 'Handles wet tracks fine.'}"
            )
        elif trainer_level == "expert":
            return (
                f"--- Expert analysis: {self.name} ---\n"
                f"  Ceiling approx {self._potential:.1f}/10 — currently at {self.speed:.1f} speed.\n"
                f"  Improves {'quickly' if self._learning_rate > 0.15 else 'slowly'} with race experience.\n"
                f"  Doping response: {'strong — high risk/reward' if self._doping_sensitivity > 1.2 else 'mild' if self._doping_sensitivity < 0.8 else 'average'}.\n"
                f"  Longevity: {'will age gracefully' if self._longevity > 0.8 else 'could drop off suddenly after peak'}."
            )
        


    def __repr__(self) -> str:
        status = "BANNED" if self.is_banned else "INJURED" if self.is_injured else "OK"
        return (
            f"Horse('{self.name}' | age={self.age} | "
            f"spd={self.speed} stm={self.stamina} acc={self.acceleration} | "
            f"fit={self.fitness} fat={self.fatigue:.0f} | {status})"
        )
    


