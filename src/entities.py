import random
import json
from dataclasses import dataclass, field
from typing import Optional


class NameGenerator:
    """
    Name Generator med dynaty och paternity regeler
    """
    PREFIXES = [
        "Storm", "Thunder", "Silver", "Dark", "Golden", "Iron", "Wild",
        "Shadow", "Swift", "Blaze", "Royal", "Steel", "Night", "Star",
        "Frost", "Norse", "Viking", "Mjölnir", "Odin", "Freya", "Saga", "Cold", "Cash",
    ]

    SUFFIXES = [
        "Runner", "Wind", "Bolt", "Flash", "Fire", "Spirit", "Arrow",
        "Dancer", "Fury", "Storm", "Blade", "Lance", "Prince", "Star",
        "Comet", "Ridge", "Dream", "Glory", "Force", "Tide",
    ]

    DYNASTY_CONNECTORS = [
        "'s Echo", "'s Legacy", "'s Pride", "'s Shadow", "'s Heir",
        "'s Thunder", " Junior", " II", " the Second",
    ]

    NOBLE_TITLES = ["Sir", "Lady", "Lord", "Baron", "Duke", "Duchess"]

    @classmethod
    def random_name(cls) -> str:

        title = random.choice(cls.NOBLE_TITLES) + " " if random.random() < 0.20 else ""
        return title + random.choice(cls.PREFIXES) + random.choice(cls.SUFFIXES)
    
    @classmethod
    def foal_name(cls, sire_name: str, dam_name: str) -> str:
        """
        Naming rules for bred horses:
          1. Paternity rule: name must START with the first letter of the father's name.
          2. 40% chance of a dynasty name (e.g. "Thunder's Echo") if sire was famous.
          3. 30% chance of a blended name (first syllable of each parent).
          4. Fallback: random name starting with sire's first letter.
        """

        sire_first_letter = sire_name[0].upper()

        if random.random() < 0.40:
            connector = random.choice(cls.DYNASTY_CONNECTORS)
            return sire_name.split()[0] + connector
        
        if random.random() < 0.30:
            sire_part = sire_name[:3]
            dam_part  = dam_name[-4:]
            blended = (sire_part + dam_part).capitalize()
            return blended
        
        valid_prefixes = [p for p in cls.PREFIXES if p.startswith(sire_first_letter)]
        if not valid_prefixes:
            valid_prefixes = cls.PREFIXES

        return random.choice(valid_prefixes) + random.choice(cls.SUFFIXES)


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
    

class Jockey:

    """
    Jockeys are 'pilots' they modify horse performance during a race.
    They can be:
      - Personal: owned by a player, trainable, improve with a specific horse.
      - Freelance: hired per-race from the market.
      - Elite: rare, bidded on at auction, can achieve stats normal jockeys can't.
    """

    TIER_RANGERS = {
        "rookie": (3.0, 5.5),
        "amateur": (4.5, 6.5),
        "pro": (6.0, 8.0),
        "elite": (7.5, 10.0),
    }

    def __init__(self,name: str,tier: str = "amateur"):
        self.name = name
        self.tier = tier


        lo, hi = self.TIER_RANGERS.get(tier, (4.0, 7.0))

        #Stats that we can see
        self.pacing = round(random.uniform(lo, hi), 2)
        self.aggresion = round(random.uniform(lo, hi), 2)
        self.stability = round(random.uniform(lo, hi), 2)


        self.races_ridden = 0
        self.wins = 0
        self.reputation = round(random.uniform(30,70),1) if tier != "elite" else round(random.uniform(70, 100), 1)


        self.is_freelance = tier != "rookie"
        self.is_elite = tier == "elite"
        self.contract_farm = None

        #roliga corruption stats som spelaren inte kan se
        self._integrity = round(random.uniform(0.5, 1.0), 2)
        self._will_fix_races = self._integrity < 0.35

        self._synergy: dict[str, float] = {}

        self.race_fee = {
            "rookie": random.randint(100, 300),
            "amateur": random.randint(300, 800),
            "pro": random.randint(800, 2500),
            "elite": random.randint(5000, 20000),
        }[tier]


    def get_synergy(self, horse_name: str) -> float:
        """
        Returns the synergy bonus for this jockey+horse pair.
        Starts at 1.0 (neutral). Every race together nudges it up.
        Max is 1.5  a 50% relationship bonus on top of base stats.

        dict.get(key, default) returns the default if key doesn't exist.
        """
        return self._synergy.get(horse_name,1.0)

    def build_synergy(self, horse_name: str):
        """
        Called after every race together. Synergy grows faster early.
        """
        current = self.get_synergy(self, horse_name)
        growth = 0.04 * (1.5 - current)
        self._synergy[horse_name] = round(min(1.5, current + growth), 3)

    def race_score_modifier(self, horse) -> float:
        """
        Returns a multiplier applied to the horse's race score.
        Formula: weighted average of jockey stats × synergy bonus.
        """

        jockey_skill = (
            self.pacing * 0.40 +
            self.aggresion * 0.35 +
            self.stability * 0.25
        )/10.0

        synergy_bonus = self.get_synergy(horse.name)
        return (0.70 + jockey_skill * 0.30) * synergy_bonus

    def offer_fix(self, race_prize: int) -> Optional[int]:
        """
        If the jockey is corruptible, they may approach the player
        offering to 'hold back'/lose on purpose.
        Returns the asking price, or None if they won't cheat.
        """

        if self._will_fix_races and random.random() < 0.15:
            asking_price = int(race_prize * random.uniform(0.1,0.3))
            return asking_price
        return None
    
    def record_race(self, won: bool):
        self.races_ridden += 1
        if won:
            self.wins += 1
            self.reputation = min(100, self.reputation + 2)
        self.race_fee = int(self.race_fee * (1.01 if won else 1.0))
    
    def __repr__(self) -> str:
        win_rate = f"{self.wins/self.races_ridden*100:.0f}%" if self.races_ridden else "n/a"
        return (f"Jockey('{self.name}' | {self.tier} | "
                f"pac={self.pacing} agg={self.aggression} stb={self.stability} | "
                f"wins={self.wins}/{self.races_ridden} [{win_rate}] | fee={self.race_fee}g)")
class Handler:
    """
    Handlers are permanent staff attached to a Farm.
    Their stats affect every horse they look after each week,
    but the player only sees the *effects* (slower decline, fewer injuries),
    not the numbers directly unless they pay for a staff review.
    """

    SPECIALISATIONS = [
        "Trainer",     # Ökad stat growth
        "Vet",         # injury
        "Nutritionist", # feed efficiency
        "Psychologist", # focus
        "Groom",       # general-purpose, billigare
    ]

    def __init__(self, name: str ,specialisation: str = None):
        self.name = name
        self.specialisation = specialisation or random.choice(self.SPECIALISATIONS)

        self.knowledge = round(random.uniform(3.0,9.0), 2)
        self.work_ethic = round(random.uniform(3.0,9.0), 2)
        self.horse_sense = round(random.uniform(3.0,9.0), 2)

        # Low integrity handlers may: steal, blackmail, leak doping info, do nothing
        self._integrity   = round(random.uniform(0.4, 1.0), 2)
        self._knows_about_doping: set = set()

        avg_skill = (self.knowledge + self.work_ethic + self.horse_sense) / 3
        self.weekly_salary = int(avg_skill * 120)

        self.assigned_farm: Optional[str] = None
        self.weeks_employed = 0

    def weekly_effect(self, horse) -> dict:
        """
        Called each game week for every horse this handler looks after.
        Returns a dict of stat modifications to apply to the horse.
        """
        effects= {}


        if self.specialisation in ("Trainer", "Groom"):
            effects["learning_boost"] = self.knowledge * 0.01
        if self.specialisation in ("Vet", "Groom"):
            injury_reduction = self.work_ethic * 0.005
            effects["injury_reduction"] = injury_reduction
        if self.specialisation == "Nutritionist":
            effects["feed_efficiency"] = 0.8 + self.knowledge * 0.02
        if self.specialisation == "Psychologist":
            effects["morale_recovery"] = self.horse_sense * 0.5
        if horse.is_doped:
            self._knows_about_doping.add(horse.name)
        
        return effects

    def consider_blackmail(self, palyer_gold: int) -> Optional[dict]:
        """
        If Handler has a low integrity and knows about doping, they may blackmail the player
        """

        if not self._knows_about_doping:
            return None
        
        blackmail_chance = (1.0 - self._integrity) * 0.4
        if random.random() > blackmail_chance:
            return None
        
        doped_horse = random.choice(list(self._knows_about_doping))
        demand = int(player_gold * random.uniform(0.03, 0.12))

        return {
            "type": "Blackmail",
            "handler": self.name,
            "horse": doped_horse,
            "demand": demand,
            "message": (
                f"A note appears under your door:\n"
                f"'I know what you did with {doped_horse}. Pay me {demand:,} gold "
                f"or the Racing Commission gets an anonymous tip."
            )
        }
    def consider_stealing(self, farm_inventory: dict) -> Optional[dict]:
        """
        Low_integrity handlers may steal
        """

        steal_chance = (1.0 - self.integrity) * 0.1
        if random.random() > steal_chance or not farm_inventory:
            return None

        item = random.choice(list(farm_inventory.keys()))
        amount_stolen = random.randint(1, max(1, farm_inventory[item]//4))
        return {
            "type":    "theft",
            "handler": self.name,
            "item":    item,
            "amount":  amount_stolen,
        }
    def __repr__(self) -> str:
        return (f"Handler('{self.name}' | {self.specialisation} | "
            f"knw={self.knowledge} eth={self.work_ethic} | salary={self.weekly_salary}g/wk)")

class Farm:

    HAY_TYPES = {
        "Basic Hay": {"cost": 10,  "morale_bonus": 0,    "fitness_bonus": 0.5},
        "Standard Hay": {"cost": 25,  "morale_bonus": 2,    "fitness_bonus": 1.0},
        "Premium Hay": {"cost": 60,  "morale_bonus": 5,    "fitness_bonus": 2.0},
        "Champion Feed":{"cost": 120, "morale_bonus": 8,    "fitness_bonus": 3.5},
    }       

    def __init__(self, name: str, capacity: int = 5, location: str = "countryside"):
        self.name      = name
        self.capacity  = capacity   
        self.location  = location
        self.prestige  = 0

        self.horses: list = []
        self.handlers: list = []

        self.inventory = {
            "Standard Hay": 20,
            "Medication": 3,
        }

        self.has_breeding_licence = False
        self.breeding_pen: list = []

        self.weekly_upkeep = 200

    @property
    def is_full(self) -> bool:
        return len(self.horses) >= self.capacity
    
    @property
    def total_weekly_cost(self) -> int:
        handlers_salaries = sum(h.weekly_salary for h in self.handlers)
        return self.weekly_upkeep + handlers_salaries

    def add_horse(self, horse) -> bool:
        """Returns True if successful, False if stall is full."""
        if self.is_full:
            print(f"  {self.name} is full! ({self.capacity} stalls taken.)")
            return False
        self.horses.append(horse)
        print(f"  {horse.name} moved into {self.name}.")
        return True

    def remove_horse(self, horse_name: str):
        self.horses = [h for h in self.horses if h.name != horse_name]
    
    def hire_handler(self, handler) -> bool:
        if len(self.handlers) >= max(2, self.capacity // 2):
            print(f" {self.name} already has enough staff.")
            return False
        handler.assigned_farm = self.name
        self.handlers.append(handler)
        return True

    def fire_handler(self, handler_name: str):
        self.handlers = [h for h in self.handlers if h.name != handler_name]
    
    def feed_horses(self, hay_type: str = "Standard Hay"):
        """
        Feeds all horses at this farm this week.
        Each handler's 'Nutritionist' bonus is applied if present.
        """
        if self.inventory.get(hay_type, 0) < len(self.horses):
            print(f" Not enough {hay_type} for all horses at {self.name}!")
            hay_type = "Basic Hay"
        
        hay_stats = self.HAY_TYPES[hay_type]
        nutritionist = next(( h for h in self.handlers if h.specialisation == "Nutritionist"), None)

        feed_multiplier = nutritionist._integrity * 1.2 if nutritionist else 1.0


        for horse in self.horses:
            horse.morale = min(100, horse.morale + hay_stats["morale_bonus"] * feed_multiplier)
            horse.fitness = min(100, horse.fitness + hay_stats["fitness_bonus"] * feed_multiplier)
        
        used = len(self.horses)
        self.inventory[hay_type] = max(0, self.inventory.get(hay_type, 0) - used)
    
    def weekly_handler_actions(self, player) -> list:
        """
        Each handler does their job, and potentially causes drama.
        Returns a list of event dicts for main.py to handle.
        """
        events = []
        
        for handler in self.handlers:
            handler.weeks_employed += 1

            for horse in self.horses:
                effects = handler.weekly_effect(horse)
                if "learning_boost" in effects:
                    horse._learning_rate = min(0.5, horse._learning_rate + effects["learning_boost"])
                if "injury_reduction" in effects:
                    horse._injury_proneness = max(0.01, horse._injury_proneness - effects["injury_reduction"])
                if "morale_recovery" in effects:
                    horse.morale = min(100, horse.morale + effects["morale_recovery"])
                
            blackmail = handler.consider_blackmail(player.gold)
            if blackmail:
                events.append(blackmail)
            
            theft = handler.consider_stealing(self.inventory)
            if theft: 
                item, amt = theft["item"], theft["amount"]
                self.inventory[item] = max(0, self.inventory.get(item, 0) - amt)
                events.append(theft)
        return events

    
    def __repr__(self) -> str:
        return (f"Farm('{self.name}' | {len(self.horses)}/{self.capacity} horses | "
                f"{len(self.handlers)} staff | upkeep={self.total_weekly_cost}g/wk)")

class Player:
    """
    The Player owns farms (which contain horses and handlers),
    a roster of personal jockeys, and tracks their reputation globally.

    Reputation matters:
      - Needed to enter prestige competitions
      - Lowered by doping scandals, blackmail going public
      - Raised by clean wins and charitable donations
    """
    REPUTATION_TIERS = {
        (0,  20):  "Disgraced",
        (20, 40):  "Unknown",
        (40, 60):  "Established",
        (60, 80):  "Respected",
        (80, 100): "Legendary",
    }

    def __init__(self, name: str, starting_gold: int = 15_000):

        self.name = name
        self.gold= starting_gold
        self.reputation = 40
        self.week = 1


        self.farms: list[Farm] = [Farm(f"{name}'s Stable", capacity=4)]
        self.jockeys: list[Jockey] = []

        self.race_history: list[dict] = []
        self.active_blackmails: list[dict] = []
        self.known_events: list[str] = []

        self.is_banned = False
        self.doping_warnings = 0















