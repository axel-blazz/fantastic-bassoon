import json
from confluent_kafka import Consumer, KafkaException
from loguru import logger
from router import route_event

REQUIRED_FIELDS = {"event_id", "event_type"}

def create_consumer() -> Consumer:
    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'ai-workers',
        'enable.auto.commit': False,
        'auto.offset.reset': 'earliest'
    })
    return consumer

def deserialize_event(raw_value: bytes) -> dict | None:
    try:
        payload = json.loads(raw_value.decode('utf-8'))
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON: {e}")
        return None
    
    missing_fields = REQUIRED_FIELDS - payload.keys()
    if missing_fields:
        logger.error(f"Missing required fields in event payload: {missing_fields}")
        return None
    
    return payload

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

            # Deserialize the event
            event = deserialize_event(msg.value())
            if event is None:
                consumer.commit(msg)
                continue  # Skip invalid messages
            
            try:
            # Handle the event based on its type
                handled = route_event(event)
                # Commit offset for both handled and non-retryable events
                consumer.commit(msg)
                if not handled:
                    logger.warning(f"Unhandled event type(Skipped and Commited): {event.get('event_type')} | ID: {event.get('event_id')}")
                # logger.info(f"Received message: {event} | Partition: {msg.partition()} | Offset: {msg.offset()}")
                else:
                    logger.info(f"Successfully handled event: {event.get('event_type')} | ID: {event.get('event_id')}")
            except Exception as e:
                logger.error(f"Error handling event {event.get('event_type')} | ID: {event.get('event_id')} | Error: {e}")

    except KeyboardInterrupt:
        logger.info("Consumer interrupted by user")
    finally:
        consumer.close()
        logger.info("Kafka consumer closed")

if __name__ == "__main__":
    run_consumer()