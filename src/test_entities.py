from entities import Player, Jockey, Handler, NameGenerator, Horse

# Create a player
player = Player("Erik Svensson", starting_gold=150_000)
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

# Buy 4 horses
for i in range(4):
    player.buy_horse(farm_index=0, cost=1500)
    print()

# Print a report for each one
horses = player.all_horses
for horse in horses:
    print(horse.trainer_report("expert"))
    print()  
    
    

# Run a week
print("--- End of Week 1 ---")
events = player.end_of_week()
for event in events:
    print(f"\n  EVENT: {event.get('message', event)}")

print(f"\n{player}")

#run 10 weeks
print("--- 3 Weeks later ---")
for i in range (3):
    events = player.end_of_week()
    for event in events:
        print(f"\n EVENT: {event.get("message", event)}")
