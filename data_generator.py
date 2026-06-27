import json, time, random, os

os.makedirs("data/stream", exist_ok=True)

actions = ["purchase", "purchase", "purchase", "view"]
while True:
    data = {
        "user_id": random.randint(1, 8),
        "product_id": random.randint(100, 110),
        "action": random.choice(actions),
        "timestamp": time.time()
    }

    filename = f"data/stream/event_{int(time.time()*1000)}.json"
    
    with open(filename, "w") as f:
        json.dump(data, f)

    print("Generated:", data)
    time.sleep(1)
