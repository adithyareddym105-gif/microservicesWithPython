# Module 5 - Reflection
**Team name**: microservicesWithPython
**Branch**: module-05
**Submitted**: before Module 6 lesson

---

## 1. Why does auth-service exist as its own service?

Auth could have been built into every service or into the gateway alone. Making it a separate service means one place issues and validates all tokens. If we need to change the signing key, the algorithm, or the token lifetime, we change it in one service and nothing else needs to be redeployed. Every other service stays decoupled from authentication logic.

---

## 2. Your choice

We implemented create_access_token to add the expiry claim before signing, and get_current_user to decode and verify the token on every protected request. The key decision was to return the full decoded payload rather than just the username - this lets any downstream service read the role and other claims directly from the token without calling auth-service again.

---

## 3. The tradeoff

JWTs are stateless - once issued, a token is valid until it expires and there is no way to revoke it early. If a user's account is compromised or deleted, their token keeps working until expiry. The tradeoff is simplicity and performance (no database lookup on every request) versus the inability to invalidate tokens instantly. A refresh token or a token blacklist would solve this but adds complexity.
