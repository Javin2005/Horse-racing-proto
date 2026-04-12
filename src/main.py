from Horse import Horse

def simulate_race(Horses, track_condition="Dry"):
    print(f"\n RACE START | Track: {track_condition}\n")


    results = []
    for h in Horses:
        if h.is_banned:
            print(f" {h.name} is banned and cannot race.")
            continue
        score = h.race_score(track_condition)
        results.append((score,h))

    
    results.sort(key = lambda x: x[0], reverse=True)

    print("Finishing order:")
    for position, (score, horse) in  enumerate(results, start=1):
        print(f" {position}. {horse.name}  (score: {score:.2f})")
    
    return results


#test
field = [Horse("Thunder"), Horse("Mjölnir"), Horse("Storm"), Horse("Blixten")]
simulate_race(field, track_condition="Muddy")
