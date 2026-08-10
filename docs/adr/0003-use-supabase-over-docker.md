# ADR 0003: Use Supabase over Local Docker

## Status
Accepted — 2026-08-09

## Context
We need a PostgreSQL database for the SBAIP platform. The options are:
- Run PostgreSQL locally in Docker
- Use a cloud-hosted PostgreSQL (Supabase)

The local Docker option would require allocating RAM (PostgreSQL ~500MB) and storage from the 16GB / 8GB constrained environment. The cloud option offloads these resources.

## Decision Drivers
- **Resource constraints:** 16GB RAM, 8GB free disk space (Edge DataOps already uses ~6GB RAM)
- **Maintenance:** Cloud provider handles backups, updates, availability
- **Cost:** Free tier available
- **Access:** Must be accessible from local Python scripts

## Decision
Use Supabase (cloud PostgreSQL) because:
- Saves ~500MB RAM and ~1GB storage on local machine
- Free tier (500 MB database, 2 GB bandwidth) is sufficient for Phase 1–2
- No Docker container to maintain
- Built-in authentication (future)
- Real-time subscriptions (future)

## Consequences

### Positive
- Frees local resources for Edge DataOps and other tools
- Automatic backups and updates
- Accessible from anywhere (not just local machine)
- Easy to share with collaborators

### Negative
- Requires internet connection
- Supabase free tier limits (500 MB database, 2 GB bandwidth)
- Vendor lock-in (but PostgreSQL can be migrated)

## Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
| :--- | :--- | :--- | :--- |
| Local Docker | Full control | Uses local resources, requires maintenance | Resource constraint |
| AWS RDS | Scalable | Expensive, complex | Overkill for Phase 1–2 |
| Heroku Postgres | Easy | Free tier very limited, sunsetting | Outdated |

## Implementation Notes
- Supabase project created
- Connection via environment variables
- Local fallback plan: Docker if internet is unavailable (future)

## References
- [Supabase Pricing](https://supabase.com/pricing)
- [PostgreSQL Docker](https://hub.docker.com/_/postgres)

## Date
2026-08-09