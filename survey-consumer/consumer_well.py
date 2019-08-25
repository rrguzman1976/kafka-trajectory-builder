from confluent_kafka import Consumer, KafkaError

from python_gis import hello as h

# TODO: Convert to read from survey-cln
# Example consumer from Debezium topic.
def main():

    wkt = h.depends_check()
    print(f"WKT: {wkt}")

    print(f"Starting Python consumer...")

    c = Consumer({
        'bootstrap.servers': 'kafka:9092',
        'group.id': 'ds-consumer-python-01',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': 'true'
    })
    
    try:
        c.subscribe(['funky-chicken.dbo.DbzWell'])
        
        iteration = 1
        while True:
            print(f"Polling {iteration}...")
            msg = c.poll(2.0)
            iteration += 1
            
            if not msg:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue

            print(f"Received message key: {msg.key().decode('utf-8')}")
            print(f"Received message: {msg.value().decode('utf-8')}")
            
            #c.commit() # if auto-commit = false
            
    except Exception as e:
        print(f"Unhandled error: {e}")
    finally:
        c.close()    

if __name__ == '__main__':
    main()