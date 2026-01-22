# 📘 Incident Intelligence Platform — Deep Learning Log

**Day 1 → Day 8 (Grounded, Non-Hallucinated)**

This document records:

- The **exact questions/confusions** I had
- **Why I was confused**
- The **precise explanation that resolved it**
- The **mental model** I should remember

This is written for **revision**, not summary.

---

## 🟦 Day 1 — PRD & Project Start

### Question I had

> “Can I just start building and refine later?”

### Why I was confused

I was used to learning by coding first and fixing later.

### Explanation that helped

- PRD defines **what must exist**, **what must not exist**, and **what is intentionally postponed**
- Code written before understanding requirements usually needs rewriting

### Mental model

> PRD = boundary  
> Code = implementation inside that boundary

---

## 🟦 Day 2 — Structure, Config & Logging

### Question I had

> “Why do we need so many folders? Why not keep logic together?”

### Why I was confused

Early projects work fine with everything mixed.

### Explanation that helped

Folders represent **change isolation**, not cleanliness.

- `schemas` → API contract (changes with clients)
- `models` → DB shape (changes with storage)
- `services` → domain logic (changes with business)
- `routers` → HTTP wiring (changes with API)

### Mental model

> Files are grouped by **reason to change**, not by type.

---

### Question I had

> “Why did my Pydantic Settings class break FastAPI OpenAPI?”

(Error: `info.title Input should be a valid string`)

### Why I was confused

I mixed `python-settings` and `pydantic.BaseSettings`.

### Explanation that helped

- FastAPI expects **plain strings** for OpenAPI metadata
- Passing `Field()` objects incorrectly leaks metadata instead of values
- Use **Pydantic Settings correctly**, don’t mix libraries

### Mental model

> Config objects should expose **values**, not schema metadata.

---

## 🟦 Day 3 — Schemas

### Question I had

> “Why do we need UserIn, UserOut, UserPatch separately?”

### Why I was confused

They all represent the same user.

### Explanation that helped

Each operation needs **different guarantees**:

- `UserIn` → validation rules
- `UserOut` → safe response (no password)
- `UserPatch` → optional, partial updates

### Mental model

> Same entity, different **intent**, different **shape**

---

## 🟦 Day 4 — Database & SQLAlchemy

### Question I had

> “I created a model — why is the table not created?”

### Why I was confused

I assumed ORM models auto-create tables.

### Explanation that helped

- SQLAlchemy models **describe structure**
- Tables are created only when:
  - `Base.metadata.create_all()` runs, or
  - migrations are applied

### Mental model

> Model ≠ Table  
> ORM ≠ Database

---

### Question I had

> “Why did `server_default=datetime.now()` break?”

(Error: `ArgumentError: expected str or ClauseElement`)

### Explanation that helped

- `server_default` runs **in the database**
- Database cannot execute Python functions
- Must use `func.now()` or DB expressions

### Mental model

> `default=` → Python  
> `server_default=` → Database

---

### Question I had

> “Why am I getting `Invalid isoformat string: 'now()'`?”

### Explanation that helped

- SQLite doesn’t understand Postgres-style `now()`
- SQLite stores timestamps as strings
- DB defaults must match DB dialect

### Mental model

> Defaults are **DB-specific**

---

## 🟦 Day 5 — Authentication

### Question I had

> “Why does Swagger OAuth UI ask for username/password when I use JWT?”

### Why I was confused

Swagger UI ≠ actual auth flow.

### Explanation that helped

- Swagger OAuth UI is for OAuth2 Password Flow
- My system uses **JWT + HTTPBearer**
- Swagger UI is optional, not authoritative

### Mental model

> Swagger is a **testing tool**, not the auth system.

---

### Question I had

> “Should role be string if DB column is Enum?”

### Explanation that helped

- In Python, use `Enum`
- In DB, store **string value**
- Convert explicitly at boundaries

### Mental model

> Enum for logic  
> String for storage

---

## 🟦 Day 6 — Incident Domain

### Question I had

> “What do you mean by status transitions?”

### Why I was confused

I thought status is just a field to update.

### Explanation that helped

- Incident lifecycle is **state-based**
- Not all transitions are valid
- Example:
  - OPEN → INVESTIGATING ✅
  - OPEN → RESOLVED ❌

### Mental model

> Status = state machine, not CRUD

---

### Question I had

> “Should IncidentStatus.OPEN and IncidentStatus.OPEN.value be the same?”

### Explanation that helped

- `.OPEN` → enum object
- `.OPEN.value` → string
- Same value, different type

### Mental model

> Use enum in logic  
> Use `.value` for DB

---

## 🟦 Day 7 — Async, PATCH & CRUD

### Question I had

> “If my route is async and DB is sync, is it blocking?”

### Explanation that helped

- FastAPI runs sync code in **threadpool**
- Event loop is not blocked
- Sync code still blocks **its thread**

### Mental model

> Async route ≠ async code  
> Threadpool protects event loop

---

### Question I had

> “Should auth functions also be async?”

### Explanation that helped

- Auth logic is CPU-bound, fast
- No I/O → no benefit from async

### Mental model

> Async is for I/O, not for everything

---

### Question I had

> “Why does empty PATCH return 200?”

### Explanation that helped

- `{}` becomes `IncidentPatch(status=None)`
- `payload is None` never triggers
- Must check **fields**, not object

### Mental model

> Empty PATCH = all fields None

---

### Question I had

> `if not var` vs `if var is None`?

### Explanation that helped

- `not var` checks **truthiness**
- `is None` checks **absence**
- PATCH requires absence detection

### Mental model

> PATCH cares about **provided vs not provided**

---

## 🟦 Day 8 — Incident Logs & Relationships

### Question I had

> “Where should relationship() be defined?”

### Explanation that helped

- ForeignKey goes on **many side**
- relationship() goes where navigation is needed
- Relationship is **ORM-level**, not DB-level

### Mental model

> DB stores relation  
> ORM expresses navigation

---

### Question I had

> “Why did relationship import fail?”

### Explanation that helped

- `relationship` is in `sqlalchemy.orm`
- Not in `sqlalchemy`

### Mental model

> ORM tools live in `sqlalchemy.orm`

---

### Question I had

> “Does ondelete='CASCADE' delete from parent or child?”

### Explanation that helped

- Defined on **child**
- Triggered by **parent delete**
- Parent delete → child rows auto-deleted

### Mental model

> Parent dies → children cleaned

---

### Question I had

> “What is lazy vs eager loading?”

### Explanation that helped

- Lazy → load when accessed
- Eager → load upfront
- N+1 problem happens with lazy loading in loops

### Mental model

> Lazy = on demand  
> Eager = in bulk

---

## 🔑 Core Mental Models I Must Retain

- Async protects event loop, not logic
- PATCH must reject empty intent
- Enum = domain truth, string = persistence
- ORM models don’t create tables
- Relationships are navigation, not storage
- Cascade protects integrity
- Lazy loading can silently kill performance

---

## 🧠 Day 9 — Refactor, Relationships & Responsibility

> **Theme:** Make the system boring, predictable, and impossible to misuse.

Day 9 was focused entirely on **correctness and architectural discipline**, not on adding features.  
The goal was to refactor the system so future work (Kafka, workers, AI) becomes safe and easy.

---

### 1. Router → Service → Repository Separation

### Initial Confusion

- Route logic felt “too abstracted”
- Business logic was hard to locate
- Most logic looked like DB interaction
- Unsure why logic wasn’t directly in routes

### What Was Wrong

- Routers were handling DB queries and commits
- Logic was spread across layers
- Hard to reuse code outside FastAPI
- Risky to extend for workers / Kafka

### Final Understanding

Each layer has a single responsibility:

#### Router

- HTTP handling only
- Authentication & role checks
- Calls service functions
- Translates domain errors to HTTP responses

#### Service

- Business rules & validations
- Orchestration logic
- Raises `ValueError` for domain failures
- No FastAPI imports

#### Repository

- SQLAlchemy queries
- Loading strategy (`selectinload`)
- Commits and refresh
- Returns objects or `None`
- No business or HTTP logic

**Key takeaway:**  
If logic should work outside HTTP, it does not belong in routers.

---

### 2. ORM Relationships — Core Concepts

### Questions Faced

- On which table should relationships be defined?
- Does `relationship()` create DB columns?
- What do `backref` and `back_populates` do?
- How do lazy and eager loading differ?

### Final Understanding

#### Database Reality

- Only `ForeignKey` creates DB relationships
- `relationship()` is ORM navigation only

ORM Navigation

```python
incident_id = Column(ForeignKey("incidents.id"))
logs = relationship(
    "IncidentLogDB",
    back_populates="incident"
)
```

Enables incident.logs and log.incident

Does not enforce DB constraints

---

### 3. backref vs back_populates

- backref creates implicit reverse links

- Harder to reason about

- Risky in large codebases

- back_populates is explicit

- Clear ownership on both sides

- Safer and preferred in production

**Final rule**: Always prefer back_populates.

---

### 4. Cascade Delete — ORM vs Database

Confusion

- “Where do I set cascade=true for DB?”

- Already used cascade="all" in relationship

Final Understanding

There are two different cascades:

**ORM-level cascade (Python safety)**

```python
relationship(
    cascade="all, delete-orphan",
    passive_deletes=True
)
```

- Prevents orphan objects

- Deletes logs when parent is deleted via ORM

**DB-level cascade (Database safety)**

```python
ForeignKey("incidents.id", ondelete="CASCADE")
```

- Enforced by the database

- Works even if ORM is bypassed

- Defined only on the child table

**Key takeaway:**
ORM cascade and DB cascade are different and both are required.

---

### 5. Lazy vs Eager Loading (N+1 Problem)

**The Problem (N+1)**

```python
incidents = db.query(IncidentDB).all()
for inc in incidents:
    inc.logs
```

- 1 query for incidents

- 1 additional query per incident

- Performance degrades rapidly

**The Solution (Eager Loading)**

```python
db.query(IncidentDB)
  .options(selectinload(IncidentDB.logs))
```

- Always 2 queries

- Predictable performance

- Loading strategy centralized in repositories

**Key takeaway:**
Loading strategy belongs in repositories, not services or routers.

---

### 6. Error Handling Normalization

### Initial Issues

- Services raised HTTPException
- Routers returned inconsistent status codes
- All exceptions mapped to 400
- Internal errors leaked to clients

### Final Understanding

**Services**

- Raise `ValueError` for domain errors
- Never import FastAPI
- Never return `None` on failure

**Routers**

- Translate errors to HTTP responses
- `ValueError("not found")` → 404
- Other `ValueError` → 400
- Uncaught `Exception` → 500
- Rollback DB session on write failures

```python
except ValueError as ve:
  status = 404 if "not found" in str(ve).lower() else 400
  raise HTTPException(status_code=status, detail=str(ve))
except Exception:
  db.rollback()
  raise HTTPException(status_code=500, detail="Internal server error")
```

**Key takeaway:**  
Errors move up, responsibilities move down.

---

## 🟦 Day 8 (continued) — PATCH Semantics

### Question I had

> "Why does empty PATCH payload return 200?"

### Why I was confused

I thought `{}` was a valid no-op request.

### Explanation that helped

- Empty PATCH signals client confusion or bug
- Must reject intent-less requests explicitly
- Enforce contract: **update intent required**

```python
if not any([patch.status, patch.priority, patch.assigned_to]):
  raise ValueError("No fields provided for update")
```

### Mental model

> Empty PATCH = 400  
> Explicit contract prevents silent bugs

---

### Question I had

> "Are sync DB calls blocking in async routes?"

### Explanation that helped

- FastAPI runs sync code in threadpool
- Event loop is not blocked
- Async DB is optional for this project

### Mental model

> Async route ≠ must use async DB

---

## 🎯 What Day 9 Achieved

**Technical**

- Correct ORM relationships with explicit `back_populates`
- Safe cascade deletes at both ORM and DB levels
- Predictable query behavior via `selectinload` in repositories
- Clean error flow from domain to HTTP

**Architectural**

- Clear layer boundaries (Router → Service → Repository)
- Services reusable outside HTTP context
- System ready for Kafka, workers, and AI
- Reduced accidental complexity

## 🟦 Day 10 — Event-Driven Architecture Fundamentals

**Theme:** Event-driven architecture fundamentals (without Kafka)  
Today was about designing contracts and boundaries, not infrastructure.

---

### Question I had

> "Isn't an event just another API payload?"

### Why I was confused

I thought events were similar to request/response schemas.

### Explanation that helped

An event is a **fact about the past**, not a command.

- ❌ `CreateIncident` (command)
- ✅ `IncidentCreated` (event)

An event:

- Is **immutable**
- Describes something that **already happened**
- Can be **safely replayed**
- Must make sense **on its own** (without DB access)

### Mental model

> Events are immutable facts, not mutable commands.

---

### Question I had

> "Why not just use Kafka directly?"

### Why I was confused

I wanted to skip the in-memory phase and go straight to infrastructure.

### Explanation that helped

Kafka is **transport**, not design.

Starting in-memory helped me:

- Freeze event schemas early
- Understand when events should be emitted
- Avoid coupling business logic to Kafka APIs
- Debug events easily via logs

Kafka later becomes a plug-in, not a rewrite.

### Mental model

> Design events first, transport second.

---

### Question I had

> "Why not put events inside `schemas/`?"

### Why I was confused

I thought all schemas belonged in one place.

### Explanation that helped

| Aspect    | API Schemas       | Event Schemas      |
| --------- | ----------------- | ------------------ |
| Scope     | External contract | Internal contract  |
| Transport | Tied to HTTP      | Transport-agnostic |
| Stability | Changes often     | Must be stable     |
| Audience  | Client-facing     | System-facing      |

Created `app/events/` for this separation to prevent future chaos.

### Mental model

> API contracts ≠ Event contracts

---

### Question I had

> "Why does every event need the same metadata?"

### Why I was confused

Metadata felt like overhead.

### Explanation that helped

Shared metadata enables:

- **Idempotency** (duplicate detection)
- **Debugging** (trace events)
- **Ordering** (causality)
- **Kafka routing** (partition keys)

Key fields that must always exist:

- `event_id`
- `event_type`
- `occurred_at`
- `source`

Also learned why:

```python
class Config:
  frozen = True
```

Events must never be mutated.

### Mental model

> Events = immutable facts with traceable metadata

---

### Question I had

> "Why not emit events from routers?"

### Why I was confused

I thought events could be emitted anywhere in the stack.

### Explanation that helped

| Layer       | Emit events? | Why                       |
| ----------- | :----------: | ------------------------- |
| Router      |      ❌      | Knows HTTP, not business  |
| Repository  |      ❌      | Knows DB, not intent      |
| **Service** |      ✅      | Knows business milestones |
| Mapper      |      ❌      | Pure translation          |
| Dispatcher  |      ❌      | Transport only            |

Services are the only correct place.

### Mental model

> Only services understand business intent.

---

### Question I had

> "Why not just log the event directly?"

### Why I was confused

I saw the event dispatcher as unnecessary abstraction.

### Explanation that helped

The dispatcher:

- Hides **how** events are transported
- Allows **swapping** logging → Kafka later
- Keeps services **clean and future-proof**

This line became the only thing services care about:

```python
event_dispatcher.emit(event)
```

### Mental model

> Abstraction hides transport, not intent.

---

### Question I had

> "Isn't this extra indirection?"

(referring to mapper functions)

### Explanation that helped

Mapper functions:

- Prevent duplication
- Centralize event creation logic
- Make services simpler
- Make Kafka migration painless
- Are easy to unit test

Key rule I learned:

> Mappers are **pure functions**. No DB, no logging, no dispatching.

### Mental model

> Mappers translate, never mutate or emit.

---

### Question I had

> "When exactly should an event be emitted?"

### Why I was confused

I wasn't sure if timing mattered.

### Explanation that helped

Always **after DB commit**. Never before.

Correct order:

```
DB commit → create event → emit event
```

Why this matters:

- Prevents **phantom events** (not persisted)
- Enables **retries** later
- Makes **idempotency** possible

### Mental model

> Commit first, emit second.

---

### Question I had

> "Are all events equal?"

### Why I was confused

I thought events were monolithic.

### Explanation that helped

| Event Type               | Visibility | Frozen? |
| ------------------------ | ---------- | ------- |
| `IncidentCreatedEvent`   | Public     | ✅      |
| `LogAttachedEvent`       | Public     | ✅      |
| `AnalysisRequestedEvent` | Private    | ❓      |

Only freeze events once you are sure:

- Downstream systems will depend on them
- You won't regret the contract

### Mental model

> Freeze contracts only when stable.

---

## 🔑 Core Insights from Day 10

- Events are immutable facts about the past, not commands
- Event schemas ≠ API schemas (different stability needs)
- Services emit events, never routers or repositories
- Event dispatcher abstracts transport (Kafka becomes plug-in)
- Emission timing: always after DB commit
- Freeze events only when downstream systems depend on them
