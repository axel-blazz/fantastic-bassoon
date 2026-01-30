from cache.event_idempotency import EventIdempotencyStore

event_idempotency = EventIdempotencyStore()

print(event_idempotency.has_processed("e2"))
event_idempotency.mark_processed("e2")
print(event_idempotency.has_processed("e2"))
