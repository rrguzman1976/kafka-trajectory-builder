import pandas as pd
import numpy as np
from confluent_kafka import Consumer, KafkaError
import time

def main():
    print(f"Starting Python consumer...")

    c = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'ds-consumer-python-01',
        'auto.offset.reset': 'earliest',
        #'enable.auto.commit': 'false'
    })
    
    try:
        c.subscribe(['funky-chicken.dbo.DbzWell'])
            
        while True:
            print(f"Polling...")
            msg = c.poll(2.0)
            #time.sleep(2)
            
            if not msg:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue

            print(f"Received message key: {msg.key().decode('utf-8')}")
            print(f"Received message: {msg.value().decode('utf-8')}")
            c.commit()

    except Exception as e:
        print(f"Unhandled error: {e}")
    finally:
        c.close()    

if __name__ == '__main__':
    main()