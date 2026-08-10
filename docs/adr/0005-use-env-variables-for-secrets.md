# ADR 0005: Use Environment Variables for Secrets

## Status

Accepted — 2026-08-09

---

## Context

The SBAIP platform requires sensitive credentials for:

- Supabase (PostgreSQL) connection
- API keys (future)
- Database passwords
- Cloud credentials (future)

These credentials must be kept out of version control (Git).

---

## Decision Drivers

- **Security:** Credentials must not be committed to Git
- **Convenience:** Must be easy to configure
- **Portability:** Must work across development environments
- **Standardization:** Follow industry best practices

---

## Decision

Use `.env` files together with the `python-dotenv` library.

### Implementation Approach

- `.env` file stores all secrets and is excluded from Git
- `.env.example` provides a template with placeholder values
- Variables are accessed using `os.getenv()` within Python applications

---

## Consequences

### Positive

- Secrets are never committed to Git
- Easy to switch between environments (local, staging, production)
- Aligns with industry-standard configuration practices
- Simplifies Supabase connection management

### Negative

- Introduces a dependency on `python-dotenv`
- Developers must remember to create a `.env` file from `.env.example`
- Environment variables are not encrypted, although the `.env` file remains excluded from source control

---

## Implementation Notes

### Source Control

- `.env` is excluded through `.gitignore`
- `.env.example` is committed to Git with placeholder values

### Python Usage

```python
from dotenv import load_dotenv
import os

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
```

---

## Environment Variables

| Variable | Description | Example |
|-----------|-------------|-----------|
| `SUPABASE_URL` | Supabase project URL | `https://xxx.supabase.co` |
| `SUPABASE_KEY` | Supabase API key | `eyJhbGciOiJIUzI1NiIs...` |
| `SUPABASE_DB` | Database name | `postgres` |
| `LOG_LEVEL` | Python logging level | `INFO` |

---

## References

1. Python Dotenv Documentation  
   https://pypi.org/project/python-dotenv/

2. Supabase Environment Variables Documentation  
   https://supabase.com/docs/guides/cli/env-variables

---

## Date

2026-08-09