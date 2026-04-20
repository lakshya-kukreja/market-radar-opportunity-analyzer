import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer

# Connect to the Redpanda broker running on your VM
producer = KafkaProducer(
    bootstrap_servers=['localhost:19092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

TOPIC_NAME = 'live-market-signals'

# Sample data for Indian markets
locations = ['Surat', 'Mumbai', 'Delhi', 'Bangalore', 'Pune']
keywords = ['cloud kitchen', 'lithium battery repair', 'ev charging station', 'co-working space', 'organic grocery']

print("🚀 Starting Live Market Radar Stream...")
print("Press Ctrl+C to stop.")

try:
    while True:
        # Generate a fake market signal
        signal = {
            "timestamp": datetime.utcnow().isoformat(),
            "location": random.choice(locations),
            "search_keyword": random.choice(keywords),
            "demand_intensity": random.randint(50, 100) # Score out of 100
        }
        
        # Send to Redpanda
        producer.send(TOPIC_NAME, signal)
        print(f"Sent: {signal}")
        
        # Wait 2 seconds before the next event
        time.sleep(2)

except KeyboardInterrupt:
    print("\n🛑 Stopping stream.")
finally:
    producer.close()