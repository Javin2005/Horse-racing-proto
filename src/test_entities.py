# test_entities.py  — run this to see everything working together

from entities import Player, Jockey, Handler, NameGenerator

# Create a player
player = Player("Erik Svensson", starting_gold=15_000)
print(player)
print()

# Check their starter farm
farm = player.farms[0]
print(farm)
print()

# Hire a handler
handler = Handler("Björn Larsson", specialisation="Trainer")
farm.hire_handler(handler)
print(f"Hired: {handler}")
print()

# Generate some horse names
print("--- Name Generator ---")
for _ in range(5):
    print(f"  {NameGenerator.random_name()}")

# Simulate a foal name
print(f"\nFoal of 'Thunder' x 'Silverwind': {NameGenerator.foal_name('Thunder', 'Silverwind')}")
print(f"Foal of 'Mjölnir' x 'Nightdancer': {NameGenerator.foal_name('Mjölnir', 'Nightdancer')}")
print()

# Hire a jockey
jockey = Jockey("Lena Holm", tier="pro")
player.hire_jockey(jockey)
print(f"Signed jockey: {jockey}")
print()

# Run a week
print("--- End of Week 1 ---")
events = player.end_of_week()
for event in events:
    print(f"\n  EVENT: {event.get('message', event)}")

print(f"\n{player}")