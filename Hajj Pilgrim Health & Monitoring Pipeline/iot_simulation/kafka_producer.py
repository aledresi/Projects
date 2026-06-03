import json
import time
import random
from datetime import datetime, timedelta, timezone
from kafka import KafkaProducer

def get_random_timestamp():
    start = datetime(2026, 5, 24, tzinfo=timezone.utc)
    end = datetime(2026, 5, 29, tzinfo=timezone.utc)
    random_second = random.randrange(int((end - start).total_seconds()))
    return (start + timedelta(seconds=random_second)).isoformat().replace("+00:00", "Z")

def generate_pilgrim_event():
    locations = ['21.4225,39.8262', '21.4055,39.8912', '21.3540,39.9015', '21.3650,39.9500',' ']
    weights = [40, 35, 15, 10, 5] 
    location = random.choices(locations, weights=weights)[0]
    heart_rate = random.randint(70, 150) if random.random() > 0.1 else None
    body_temperature = round(random.normalvariate(37.0, 2), 1) if random.random() > 0.1 else None

    return {
        'pilgrim_id': f'PILGRIM_{random.randint(100000, 999999)}',
        'timestamp': get_random_timestamp(),
        'current_location': location,
        'heart_rate': heart_rate,
        'body_temperature': body_temperature,
    }

KAFKA_BOOTSTRAP_SERVERS = ['localhost:29092', 'localhost:29093', 'localhost:29094']
TOPIC_NAME = 'pilgrim-movements'

def main():
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    print("the producer is working . . .")
    try:
        while True:
            producer.send(TOPIC_NAME, value=generate_pilgrim_event())
            time.sleep(0.001)
    except KeyboardInterrupt:
        producer.close()

if __name__ == '__main__':
    main()