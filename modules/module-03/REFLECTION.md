# Module 3 — Reflection
**Team name**: microservicesWithPython
**Branch**: `module-03/microservicesWithPython`
**Submitted**: before Module 4 lesson

---

## 1. The Gateway
Without a gateway, what would a frontend app need to hardcode?
What happens when a service moves to a different port or machine?

> *Your answer:*
> Without a gateway, the frontend would need to hardcode the address and port of every service — user-service on 8001, game-service on 8002, and so on. If any service moves to a different port or machine, every frontend client breaks and needs to be updated. The gateway acts as a single stable entry point: services can move or be replaced behind it without the frontend ever knowing. It also means we only expose one public address instead of several.

---

## 2. Two calls, two behaviors
User validation blocks the activity from being saved.
Game enrichment is optional — the activity saves regardless.

What is the consequence for the data if you skip user validation?
What is the consequence if you block on a missing game?

> *Your answer:*
> If we skip user validation, we end up saving activities that reference user IDs that don't exist — the database fills with orphaned records that can never be meaningfully displayed or queried. That is a data integrity problem that is hard to clean up later. On the other hand, if we block on a missing game, we reject a valid user action simply because game-service happens to be down or slow. The activity itself is real and should be recorded. Game data is enrichment — nice to have in the response, but not a reason to lose the event entirely. The two risks are different: one is about corrupting data, the other is about unnecessary availability loss.

---

## 3. Chain latency
If three services each take 1 second, how long does the user wait?
What if one of them goes down entirely?

> *Your answer:*
> If three services are called sequentially and each takes 1 second, the user waits at least 3 seconds — latency adds up in a chain. If one service goes down entirely and there is no timeout or fallback, the request hangs until it times out, which could mean the user waits indefinitely or gets a hard error. This is why the game-service call is designed to fail gracefully: it has a bounded retry window and defaults to null instead of blocking forever. For the user validation call, a 503 is returned quickly rather than hanging, so the system stays predictable even under partial failure.

---
*Keep this file. You will refer back to it during the oral presentation.*