# Module 6 - Reflection
**Team name**: microservicesWithPython
**Branch**: module-05
**Submitted**: before final presentation

---

## 1. Why does notification-service exist as a separate consumer?

Notification-service runs independently and consumes messages from RabbitMQ whenever it is ready. Activity-service does not know or care whether notification-service is running. This means the two services are completely decoupled - one can be restarted, updated, or scaled without affecting the other. If notification-service is down, messages wait in the queue and are processed when it comes back up.

---

## 2. Your choice

We store notifications in SQLite locally in notification-service rather than calling back to another service. This keeps the notification history self-contained and readable via a simple GET endpoint. The tradeoff is that notifications live on one machine, but for this stage of the system it is the simplest approach that works.

---

## 3. The tradeoff

The consumer processes one message at a time. If a large burst of activities comes in, messages queue up in RabbitMQ and notification-service processes them sequentially. This is fine for low traffic but would need multiple consumers or a worker pool to scale. The benefit is simplicity - no race conditions, no duplicate processing.
