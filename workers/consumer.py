import json
from confluent_kafka import Consumer, KafkaException
from loguru import logger
from workers.router import route_event
from cache.event_idempotency import EventIdempotencyStore

idempotency_store = EventIdempotencyStore()

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
                # Poison event(will cause issue if not committed, so commit and skip)
                consumer.commit(msg)
                continue  # Skip invalid messages

            
            try:
                event_id = event.get("event_id")

                # 🛑 Idempotency guard
                if idempotency_store.has_processed(event_id):
                    logger.warning(
                        f"Duplicate event detected — skipping | "
                        f"type={event.get('event_type')} id={event_id}"
                    )
                    consumer.commit(msg)
                    continue

                # Handle the event
                handled = route_event(event)

                if handled:
                    # ✅ Mark FIRST, then commit
                    idempotency_store.mark_processed(event_id)
                    consumer.commit(msg)
                    logger.info(
                        f"Successfully handled event | "
                        f"type={event.get('event_type')} id={event_id}"
                    )
                else:
                    # Non-retryable, but not processed
                    consumer.commit(msg)
                    logger.warning(
                        f"Unhandled event type — skipped | "
                        f"type={event.get('event_type')} id={event_id}"
                    )

            except Exception as e:
                # ❌ DO NOT commit here
                logger.error(
                    f"Error handling event | "
                    f"type={event.get('event_type')} id={event_id} | error={e}"
                )

    except KeyboardInterrupt:
        logger.info("Consumer interrupted by user")
    finally:
        consumer.close()
        logger.info("Kafka consumer closed")

if __name__ == "__main__":
    run_consumer()