# ai200_module10_servicebus — Service Bus Queues, Topics & DLQ Handling

Starter project for **AI-200 Module 10**. You provision a Service Bus
namespace, create a queue + a topic with two filtered subscriptions,
exercise a producer/consumer with retry + DLQ, then drain the DLQ.

## What's already scaffolded

| Path | Purpose |
| --- | --- |
| `lib/sb_producer.py` | `send_queue_message` (5a), `publish_topic_message` (5b) TODOs |
| `lib/sb_consumer.py` | `receive_queue_loop` (Step 7) TODO |
| `lib/dlq_handler.py` | Complete — `drain_dlq` |
| `scripts/produce_queue.py` | Send N queue messages, optionally with poison flag |
| `scripts/consume_queue.py` | Process queue messages; raises on `_force_failure` to exercise DLQ |
| `scripts/publish_topic.py` | Publish events with application properties |
| `scripts/consume_subscription.py` | Read one subscription |
| `scripts/drain_dlq.py` | Drain or resubmit dead-lettered messages |
