# Deployment & Production Readiness

Answer each question in 3-5 sentences. Be specific and practical.

---

## 1. State Management & Checkpointing

In this challenge you used `MemorySaver` for checkpointing (in-memory, single process).
In production with thousands of concurrent users, what checkpointing strategy would you use?
What are the trade-offs between different persistence backends (PostgreSQL, Redis, DynamoDB, etc.)?

**Your answer:**

---

## 2. Observability & Monitoring

How would you monitor this agent in production?
What metrics would you track? How would you detect when the router is misclassifying queries?
How would you implement logging for debugging conversation flows?

**Your answer:**

---

## 3. Knowledge Base Management

The business teams frequently update product information, promotions, and policies.
How would you design the system so the Knowledge Base can be updated without redeploying the application?
What are the pros/cons of storing the KB in code vs. a database vs. a CMS?

**Your answer:**

---

## 4. Scaling & Performance

If this bot needs to handle 10,000 concurrent conversations, what architectural changes would you make?
Consider: LLM API rate limits, latency requirements (< 5s response time), cost optimization strategies.

**Your answer:**

---

## 5. Testing Strategy

How would you test this agent beyond the manual inline.py testing used in this challenge?
Describe your approach to: unit tests for individual agents, integration tests for the full graph,
LLM output quality evaluation, and regression testing when the KB changes.

**Your answer:**

---

## 6. Security & Guardrails

What security concerns exist with this architecture (prompt injection, data leakage, etc.)?
How would you prevent the bot from generating harmful or incorrect content?
How would you handle API key management and secrets in a production deployment?

**Your answer:**
