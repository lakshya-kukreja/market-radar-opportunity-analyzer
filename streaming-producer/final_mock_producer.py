import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['localhost:19092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

TOPIC_NAME = 'live-market-signals'

locations = ['Surat', 'Mumbai', 'Delhi', 'Bangalore', 'Pune']
keywords = ['cloud kitchen', 'lithium battery repair', 'ev charging station', 'co-working space', 'organic grocery']

print("🚀 Starting Live Market Radar Stream...")
print("Press Ctrl+C to stop.")

try:
    while True:
        # Schema matched exactly to what dbt expects!
        signal = {
            "timestamp": datetime.utcnow().isoformat(),
            "city": random.choice(locations),
            "search_term": random.choice(keywords),
            "search_volume": random.randint(10, 1000), 
            "sentiment_score": round(random.uniform(-1.0, 1.0), 2) # Score from -1.0 to 1.0
        }
        
        producer.send(TOPIC_NAME, signal)
        print(f"Sent: {signal}")
        time.sleep(2)

except KeyboardInterrupt:
    print("\n🛑 Stopping stream.")
finally:
    producer.close()    