# Module 4 - Reflection
**Team name**: microservicesWithPython
**Branch**: module-04
**Submitted**: before Module 5 lesson

---

## 1. Why async messaging?

Without async messaging, activity-service would have to call notification-service directly over HTTP and wait for a response before returning to the user. This creates tight coupling - if notification-service is slow or down, the user's request fails or hangs even though the activity was saved successfully. With RabbitMQ, activity-service drops a message and moves on instantly. Notification-service can consume it whenever it is ready. The two services no longer need to be alive at the same time.

---

## 2. Your choice

We publish the message to RabbitMQ after saving the activity to the database, not before. This order matters because if we published first and then the database write failed, we would have sent a notification about an activity that does not actually exist. By saving first, we guarantee the activity is real before we tell anyone about it. The message reflects something that actually happened.

---

## 3. The tradeoff

Fire-and-forget means we lose delivery guarantees on the notification side. If RabbitMQ is down at the moment we publish, the message is lost and notification-service never finds out about the activity. We also have no way to know from activity-service whether the notification was actually processed or not. This is the cost of decoupling - we gain speed and resilience on the publishing side, but we give up certainty about what happens downstream.
