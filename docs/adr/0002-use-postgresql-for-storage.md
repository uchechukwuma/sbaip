# ADR 0002: Use PostgreSQL (Supabase) for Storage

## Status
Accepted — 2026-08-09

## Context
We need a database to store the 785+ assets extracted from IFC files. The database must support:
- Relational queries (assets, storeys, spaces, properties)
- Flexible property storage (different assets have different property sets)
- Cloud hosting (to save local resources)
- Integration with Python data pipeline
- Future API and dashboard access

Options considered:
- PostgreSQL (via Supabase)
- MongoDB (NoSQL)
- SQLite (local)
- MySQL

## Decision Drivers
- **Query flexibility:** Need to query by asset type, location, properties
- **Cloud hosting:** Save local RAM and storage (16GB constraint)
- **Integration:** Must work with Python (FastAPI, Streamlit)
- **Cost:** Free tier available
- **SQL familiarity:** Standard query language

## Decision
Use PostgreSQL hosted on Supabase because:
- Open-source, industry standard
- Cloud-hosted (Supabase free tier)
- Supports JSONB for flexible properties (EAV pattern)
- Integrates with FastAPI, Streamlit, and Python
- Free tier: 500 MB database, 2 GB bandwidth
- Built-in authentication (future)
- Real-time subscriptions (future)

## Consequences

### Positive
- Reduces local resource consumption (RAM, storage)
- Enables complex queries (joins, filters, aggregations)
- JSONB allows flexible property storage without schema changes
- PostgreSQL is widely used in industry
- Supabase provides an easy-to-use dashboard

### Negative
- Requires internet connection
- Supabase free tier has limits (500 MB, 2 GB bandwidth)
- Proprietary lock-in to Supabase (but PostgreSQL is open-source)

## Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
| :--- | :--- | :--- | :--- |
| MongoDB | Flexible schema | No complex joins, different query language | Relational queries are needed |
| SQLite | Lightweight, local | No cloud, limited concurrency | Cannot offload local resources |
| MySQL | Reliable | No native JSONB support (weaker flexible storage) | PostgreSQL is better for JSON |

## Implementation Notes
- Database: Supabase (PostgreSQL 15+)
- Connection: Environment variables (`.env`)
- Schema: `src/load/db_schema.sql`
- Loader: `src/load/load_to_db.py`
- Tables: `assets`, `storeys`, `spaces`, `asset_properties`

## References
- [Supabase Documentation](https://supabase.com/docs)
- [PostgreSQL JSONB](https://www.postgresql.org/docs/current/datatype-json.html)
- [ADR 0003](0003-use-supabase-over-docker.md) — Supabase over Docker

## Date
2026-08-09