import json
from confluent_kafka import Consumer, KafkaException
from loguru import logger

def create_consumer() -> Consumer:
    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'ai-workers',
        'enable.auto.commit': False,
        'auto.offset.reset': 'earliest'
    })
    return consumer

def run_consumer():
    consumer = create_consumer()
    topic = "incident.events"
    consumer.subscribe([topic])
    logger.info(f"Subscribed to Kafka topic: {topic}")

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue  # No message received
            if msg.error():
                raise KafkaException(msg.error())

            # Process the message
            logger.info(f"Received message: {msg.value().decode('utf-8')} | Partition: {msg.partition()} | Offset: {msg.offset()}")

            # Manually commit the message offset
            # consumer.commit(msg)

    except KeyboardInterrupt:
        logger.info("Consumer interrupted by user")
    finally:
        consumer.close()
        logger.info("Kafka consumer closed")

if __name__ == "__main__":
    run_consumer()