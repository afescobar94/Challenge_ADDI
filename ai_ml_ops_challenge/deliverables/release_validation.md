# Release Validation Evidence

Generated: 2026-04-02T00:20:40.680146Z

## 1. Automated Test Suite
- Command: `pytest -q`
- Result: `26 passed`

## 2. End-to-End Exhaustive Matrix
- Total scenarios executed: **51**
- Passed: **51**
- Failed: **0**

### 2.1 Core Matrix (8 users x 6 scenarios)
| User | Scenario | Expected Topic | Actual Topic | Agent | Pass |
|---|---|---|---|---|---|
| user_001 | saludo | SALUDO | SALUDO | handle_general | YES |
| user_001 | productos | PRODUCTOS | PRODUCTOS | handle_products | YES |
| user_001 | pagos | PAGOS | PAGOS | handle_payments | YES |
| user_001 | operaciones | PEDIDOS | PEDIDOS | handle_operations | YES |
| user_001 | cuenta_seguridad | CUENTA | CUENTA | handle_platform | YES |
| user_001 | fuera_de_alcance | FUERA_DE_ALCANCE | FUERA_DE_ALCANCE | handle_general | YES |
| user_002 | saludo | SALUDO | SALUDO | handle_general | YES |
| user_002 | productos | PRODUCTOS | PRODUCTOS | handle_products | YES |
| user_002 | pagos | PAGOS | PAGOS | handle_payments | YES |
| user_002 | operaciones | PEDIDOS | PEDIDOS | handle_operations | YES |
| user_002 | cuenta_seguridad | CUENTA | CUENTA | handle_platform | YES |
| user_002 | fuera_de_alcance | FUERA_DE_ALCANCE | FUERA_DE_ALCANCE | handle_general | YES |
| user_003 | saludo | SALUDO | SALUDO | handle_general | YES |
| user_003 | productos | PRODUCTOS | PRODUCTOS | handle_products | YES |
| user_003 | pagos | PAGOS | PAGOS | handle_payments | YES |
| user_003 | operaciones | PEDIDOS | PEDIDOS | handle_operations | YES |
| user_003 | cuenta_seguridad | CUENTA | CUENTA | handle_platform | YES |
| user_003 | fuera_de_alcance | FUERA_DE_ALCANCE | FUERA_DE_ALCANCE | handle_general | YES |
| user_004 | saludo | SALUDO | SALUDO | handle_general | YES |
| user_004 | productos | PRODUCTOS | PRODUCTOS | handle_products | YES |
| user_004 | pagos | PAGOS | PAGOS | handle_payments | YES |
| user_004 | operaciones | PEDIDOS | PEDIDOS | handle_operations | YES |
| user_004 | cuenta_seguridad | CUENTA | CUENTA | handle_platform | YES |
| user_004 | fuera_de_alcance | FUERA_DE_ALCANCE | FUERA_DE_ALCANCE | handle_general | YES |
| user_005 | saludo | SALUDO | SALUDO | handle_general | YES |
| user_005 | productos | PRODUCTOS | PRODUCTOS | handle_products | YES |
| user_005 | pagos | PAGOS | PAGOS | handle_payments | YES |
| user_005 | operaciones | PEDIDOS | PEDIDOS | handle_operations | YES |
| user_005 | cuenta_seguridad | CUENTA | CUENTA | handle_platform | YES |
| user_005 | fuera_de_alcance | FUERA_DE_ALCANCE | FUERA_DE_ALCANCE | handle_general | YES |
| user_006 | saludo | SALUDO | SALUDO | handle_general | YES |
| user_006 | productos | PRODUCTOS | PRODUCTOS | handle_products | YES |
| user_006 | pagos | PAGOS | PAGOS | handle_payments | YES |
| user_006 | operaciones | PEDIDOS | PEDIDOS | handle_operations | YES |
| user_006 | cuenta_seguridad | CUENTA | CUENTA | handle_platform | YES |
| user_006 | fuera_de_alcance | FUERA_DE_ALCANCE | FUERA_DE_ALCANCE | handle_general | YES |
| user_007 | saludo | SALUDO | SALUDO | handle_general | YES |
| user_007 | productos | PRODUCTOS | PRODUCTOS | handle_products | YES |
| user_007 | pagos | PAGOS | PAGOS | handle_payments | YES |
| user_007 | operaciones | PEDIDOS | PEDIDOS | handle_operations | YES |
| user_007 | cuenta_seguridad | CUENTA | CUENTA | handle_platform | YES |
| user_007 | fuera_de_alcance | FUERA_DE_ALCANCE | FUERA_DE_ALCANCE | handle_general | YES |
| user_008 | saludo | SALUDO | SALUDO | handle_general | YES |
| user_008 | productos | PRODUCTOS | PRODUCTOS | handle_products | YES |
| user_008 | pagos | PAGOS | PAGOS | handle_payments | YES |
| user_008 | operaciones | PEDIDOS | PEDIDOS | handle_operations | YES |
| user_008 | cuenta_seguridad | CUENTA | CUENTA | handle_platform | YES |
| user_008 | fuera_de_alcance | FUERA_DE_ALCANCE | FUERA_DE_ALCANCE | handle_general | YES |

### 2.2 Returns Multi-turn Flow
| Scenario | Prompt | Expected Topic | Actual Topic | Expected Step | Actual Step | Pass |
|---|---|---|---|---|---|---|
| returns_start | Quiero devolver un producto | DEVOLUCIONES | DEVOLUCIONES | returns_step_1_collect_order | returns_step_1_collect_order | YES |
| returns_order | ORD-2025-078 | DEVOLUCIONES | DEVOLUCIONES | returns_step_1_collect_reason | returns_step_1_collect_reason | YES |
| returns_reason | 2 | DEVOLUCIONES | DEVOLUCIONES | None | None | YES |

## 3. Inline Script Validation (`tests/inline.py`)
Executed interactively via stdin piping:

- Command:
  - `printf 'Hola\nQue promociones hay?\nQuiero devolver un producto\nORD-2025-078\n2\nQue hora es?\nexit\n' | .venv/bin/python tests/inline.py`
- Observed outcomes:
  - `SALUDO` routed to `handle_general`
  - `PRODUCTOS` routed to `handle_products`
  - `DEVOLUCIONES` flow engaged with `current_step` tracking
  - out-of-scope prompt routed to `FUERA_DE_ALCANCE`
- Result: interactive end-to-end behavior validated using the challenge script.

## 4. Checklist Assertions
- Routing by topic/agent validated across all major domains.
- Returns multi-step continuity validated (start -> order -> reason).
- Security/out-of-scope guardrails validated in end-to-end prompts.
- Architecture and MLOps deliverables completed and aligned.
- No restricted files were changed during release closure.
