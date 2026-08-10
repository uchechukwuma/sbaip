# Software Requirements Specification
## Smart Building Asset Intelligence Platform (SBAIP)

**Version:** 0.1.0
**Date:** 2026-08-09
**Status:** Phase 1 Complete — IFC Extraction

---

## 1. Introduction

### 1.1 Purpose
Transform Building Information Models (BIM) into a living digital asset management system by integrating:
- Building Information (IFC/BIM)
- IoT sensor data (simulated/real)
- Cloud data engineering
- Analytics
- Interactive dashboards

### 1.2 Scope
The platform extracts assets from IFC files, stores them in a PostgreSQL database (Supabase), provides a REST API, and displays a dashboard. Initially focused on architectural models, with future support for MEP and sensor data.

### 1.3 Definitions

| Term | Definition |
| :--- | :--- |
| **Digital Twin** | Virtual representation that updates with real-time data |
| **Asset** | Any building component (wall, door, HVAC, etc.) |
| **IFC** | Industry Foundation Classes — open standard for BIM data |
| **SBAIP** | Smart Building Asset Intelligence Platform |
| **BIM** | Building Information Modeling |
| **Supabase** | Open-source Firebase alternative with PostgreSQL |
| **EAV** | Entity-Attribute-Value pattern for flexible properties |

### 1.4 Target Audience
- **Facility Managers** — End users of the dashboard
- **Data Engineers** — Developers extending the platform
- **Researchers** — Evaluating digital twin architectures
- **GATE Reviewers** — Assessing project scope and feasibility
- **Thesis Supervisors** — Evaluating academic rigor

### 1.5 Relationship to Edge DataOps Platform
SBAIP extends an existing IoT data pipeline (Edge DataOps Platform) to the building management domain.

**Reused Components:**
- EMQX MQTT broker → sensor ingestion
- Kafka → event streaming (15k+ msg/sec capacity)
- Apache Airflow → orchestration
- dbt → SQL transformations
- Great Expectations → data quality validation
- MongoDB Atlas → time-series storage
- Supabase → operational storage (reused for SBAIP)
- Streamlit → dashboard framework

**New Components:**
- IFC/BIM parser (Python + IfcOpenShell)
- Building hierarchy data model (PostgreSQL/Supabase)
- Asset health scoring logic
- Maintenance scheduling module
- Building-specific dashboard visualizations

---

## 2. Functional Requirements

### FR-01: IFC Parsing -- COMPLETED (v0.1.0)

**Description:** Extract structured asset data from IFC files.

**Requirements:**
- Extract all assets with GlobalId, Name, Type, ObjectType
- Extract spatial hierarchy (Site → Building → Storey → Space)
- Extract property sets (Pset_*, PSet_Revit_*)
- Support IFC2x3 and IFC4
- Save output as CSV, JSON, and database tables

**Implementation:**
- Script: `src/extract/ifc_parser.py`
- Library: IfcOpenShell (Python)
- Status:  Implemented

**Results:**
| Metric | Value |
| :--- | :--- |
| **Total Assets Extracted** | 785 |
| **Asset Types** | 15 IFC classes |
| **Properties Extracted** | 327 columns |
| **Storeys** | 4 |
| **Spaces** | 21 |
| **IFC Files Processed** | 2 (IFC2x3 + IFC4) |

**Asset Breakdown:**
| Asset Type | Count |
| :--- | :--- |
| IfcProduct | 295 |
| IfcElement | 268 |
| IfcWall | 57 |
| IfcWallStandardCase | 56 |
| IfcWindow | 24 |
| IfcSlab | 21 |
| IfcSpace | 21 |
| IfcDoor | 14 |
| IfcCovering | 13 |
| IfcBeam | 8 |
| IfcBuildingStorey | 4 |
| IfcStair | 2 |
| IfcRoof | 1 |
| IfcBuilding | 1 |

---

### FR-02: Asset Database 🔲 IN PROGRESS (v0.2.0)

**Description:** Store assets in PostgreSQL (Supabase) with flexible property support.

**Requirements:**
- Store all assets with GlobalId as primary key
- Store spatial hierarchy (storeys, spaces)
- Support flexible properties (EAV pattern)
- Enable queries by asset type, location, property
- Use Supabase for cloud hosting (saves local resources)

**Implementation:**
- Database: Supabase (cloud PostgreSQL)
- Schema: `src/load/db_schema.sql`
- Loader: `src/load/load_to_db.py`
- Connection: Environment variables (`.env`)

**Status:** 🔲 In Progress (v0.2.0)

---

### FR-03: Sensor Simulator 🔲 PLANNED (v0.3.0)

**Description:** Generate realistic IoT sensor data for testing.

**Requirements:**
- Temperature: 18–26°C (simulate diurnal variation)
- CO₂: 400–1200 ppm (simulate occupancy patterns)
- Energy consumption: kWh (simulate building usage)
- Time-series data generation with timestamps
- Output: MQTT or Kafka topics

**Implementation:**
- Python simulation script
- Schedule: Airflow DAG or cron
- Data format: JSON with timestamp, sensor_id, value

**Status:** 🔲 Planned (v0.3.0)

---

### FR-04: REST API 🔲 PLANNED (v0.4.0)

**Description:** Provide programmatic access to building data.

**Requirements:**
- GET /assets — list all assets (with filtering)
- GET /assets/{id} — get asset details
- GET /assets/{id}/properties — get asset properties
- GET /assets/by-type/{type} — filter by IFC class
- GET /assets/by-storey/{storey} — filter by location
- GET /spatial — get spatial hierarchy

**Implementation:**
- Framework: FastAPI (Python)
- Database: Supabase (PostgreSQL)
- Authentication: Supabase Auth (future)

**Status:** 🔲 Planned (v0.4.0)

---

### FR-05: Dashboard 🔲 PLANNED (v0.5.0)

**Description:** Interactive dashboard for facility managers.

**Requirements:**
- Building summary (floors, rooms, assets)
- Asset list with search and filter
- Asset detail view with all properties
- Alerts (maintenance due, thresholds exceeded)
- Visual navigation (tree view or 3D floor plan)

**Implementation:**
- Framework: Streamlit or React
- Data: FastAPI endpoints
- Deployment: Streamlit Cloud or local

**Status:** 🔲 Planned (v0.5.0)

---

## 3. Non-Functional Requirements

### NFR-01: Performance
| Requirement | Target | Status |
| :--- | :--- | :--- |
| Parse 100MB IFC | < 2 minutes | ✅ Met |
| API response | < 200ms | 🔲 Not yet tested |
| Dashboard load | < 3 seconds | 🔲 Not yet tested |
| Query 10,000 assets | < 1 second | 🔲 Not yet tested |

### NFR-02: Maintainability
| Requirement | Target | Status |
| :--- | :--- | :--- |
| Test coverage | 80% | 🔲 Planned |
| CI/CD | GitHub Actions | 🔲 Planned |
| Documentation | ADRs, SRS, README | ✅ Complete for Phase 1 |
| Code quality | Python best practices | 🔲 In Progress |

### NFR-03: Data Quality
| Requirement | Implementation | Status |
| :--- | :--- | :--- |
| Log extraction warnings | Python logging | ✅ Implemented |
| Handle missing properties | Graceful fallbacks | ✅ Implemented |
| Validate data types | Type checking | 🔲 Planned |
| Data lineage | Logging | 🔲 Planned |

### NFR-04: Reproducibility
| Requirement | Implementation | Status |
| :--- | :--- | :--- |
| Database container | Supabase (cloud) | ✅ Decided |
| Python environment | venv + requirements.txt | ✅ Implemented |
| Documentation | Git + ADRs | ✅ Implemented |
| Data source tracking | IFC file metadata | ✅ Implemented |

### NFR-05: Resource Constraints
| Resource | Constraint | Solution |
| :--- | :--- | :--- |
| RAM | 16 GB (15.7 GB usable) | Supabase instead of local Docker |
| Storage | 45 GB free | Minimal local storage |
| Docker | Already running | Use Supabase to avoid additional containers |

---

## 4. Technology Stack

| Layer | Technology | Status | Rationale |
| :--- | :--- | :--- | :--- |
| Data Extraction | Python + IfcOpenShell | ✅ Implemented | Open source, cross-platform |
| Database | Supabase (PostgreSQL) | 🔲 In Progress | Cloud-hosted, saves local resources |
| API | FastAPI | 🔲 Planned | Modern, fast, Python-native |
| Dashboard | Streamlit | 🔲 Planned | Quick prototyping, Python |
| Orchestration | Apache Airflow | 🔲 Planned | Reused from Edge DataOps |
| Data Quality | Great Expectations | 🔲 Planned | Reused from Edge DataOps |
| CI/CD | GitHub Actions | 🔲 Planned | Free, integrates with GitHub |
| Version Control | Git + GitHub | ✅ Implemented | Industry standard |
| Documentation | Markdown + ADRs | ✅ Implemented | Lightweight, versioned |

---

## 5. Milestones

| Milestone | Version | Focus | Status | Completion Date |
| :--- | :--- | :--- | :--- | :--- |
| M1 | v0.1.0 | IFC Extraction | ✅ Completed | 2026-08-09 |
| M2 | v0.2.0 | Database + Load | 🔲 In Progress | TBD |
| M3 | v0.3.0 | Sensor Simulator | 🔲 Planned | TBD |
| M4 | v0.4.0 | REST API | 🔲 Planned | TBD |
| M5 | v0.5.0 | Dashboard | 🔲 Planned | TBD |
| M6 | v1.0.0 | Production Ready | 🔲 Planned | TBD |

---

## 6. Architecture Decision Records (ADRs)

| ADR | Title | Status | Date |
| :--- | :--- | :--- | :--- |
| ADR 0001 | Use IfcOpenShell for IFC Parsing | ✅ Accepted | 2026-08-09 |
| ADR 0002 | Use PostgreSQL (Supabase) for Storage | ✅ Accepted | 2026-08-09 |
| ADR 0003 | Use Supabase over Local Docker | ✅ Accepted | 2026-08-09 |
| ADR 0004 | IFC Extraction Approach — Phase 1 | ✅ Completed | 2026-08-09 |
| ADR 0005 | Use Environment Variables for Secrets | ✅ Accepted | 2026-08-09 |

---

## 7. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
| :--- | :--- | :--- | :--- |
| Supabase free tier limits | Low | Medium | Monitor usage, upgrade if needed |
| Internet required for Supabase | Medium | Low | Local fallback plan (Docker) if needed |
| IFC file size > 500MB | Low | High | Use smaller models, optimize parser |
| Property value truncation | Medium | Medium | Review truncation limits, expand if needed |
| Data privacy in cloud | Low | Medium | Use anonymized data, review Supabase compliance |

---

## 8. Revision History

| Version | Date | Author | Changes |
| :--- | :--- | :--- | :--- |
| 0.1.0 | 2026-08-09 | Uchechukwu Obi | Initial draft — Phase 1 complete |
| 0.1.1 | 2026-08-09 | Uchechukwu Obi | Added Target Audience, Supabase decisions, updated ADRs |

---

## 9. References

- [ADR 0001](adr/0001-use-ifcopenshell-for-parsing.md) — IfcOpenShell Decision
- [ADR 0002](adr/0002-use-postgresql-for-storage.md) — PostgreSQL Decision
- [ADR 0003](adr/0003-use-supabase-over-docker.md) — Supabase Decision
- [ADR 0004](adr/0004-ifc-extraction-approach.md) — Phase 1 Approach
- [ADR 0005](adr/0005-use-env-variables.md) — Environment Variables
- [CHANGELOG](changelog.md) — Project Changelog
- [buildingSMART IFC Standards](https://www.buildingsmart.org/standards/)
- [Supabase Documentation](https://supabase.com/docs)

---

## 10. Appendices

### Appendix A: Sample Data — Duplex Apartment

**File:** `Duplex_A_20110907.ifc`
**Format:** IFC2x3
**Size:** ~5 MB
**Assets Extracted:** 785
**Property Sets Found:** Pset_WallCommon, Pset_DoorCommon, Pset_WindowCommon, Pset_SlabCommon, Pset_RoofCommon, Pset_BeamCommon, Pset_StairCommon, Pset_SpaceCommon, PSet_Revit_*

### Appendix B: Sample Data — PCERT Scene

**File:** `Building-Architecture.ifc`
**Format:** IFC4
**Size:** ~500 KB
**Assets Extracted:** 49
**Purpose:** IFC4 compatibility validation

### Appendix C: Glossary

| Term | Definition |
| :--- | :--- |
| EAV | Entity-Attribute-Value — flexible schema pattern |
| IFC | Industry Foundation Classes — BIM data standard |
| MEP | Mechanical, Electrical, Plumbing |
| BIM | Building Information Modeling |
| Digital Twin | Virtual representation of physical asset |
| GUID | Globally Unique Identifier (IFC GlobalId) |

---

## 11. Changelog

| Version | Date | Changes |
| :--- | :--- | :--- |
| 0.1.0 | 2026-08-09 | Initial release — Phase 1 complete |