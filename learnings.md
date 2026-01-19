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

## 🟢 Ready for Day 9

I now understand:
- Why refactor is needed
- What must stay unchanged
- Where performance traps exist
- How to refactor safely

This document is my **revision anchor** before moving forward.
