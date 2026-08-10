# Changelog

All notable changes to SBAIP will be documented in this file.

The format is based on https://keepachangelog.com/en/1.0.0/,
and this project adheres to Semantic Versioning
---

## [0.1.0] - 2026-08-09 — Phase 1: IFC Extraction Complete

### Summary

Phase 1 delivers a fully functional IFC asset extraction pipeline that transforms BIM models into structured data ready for database loading. The platform successfully extracts 785 assets from IFC2x3 models and 49 assets from IFC4 models, demonstrating compatibility with both major IFC versions.

---

### Added

#### Core Features

- **IFC Parser Script** (`src/extract/ifc_parser.py`) using IfcOpenShell
  - Extracts architectural elements: walls, doors, windows, slabs, roofs, beams, stairs, spaces
  - Extracts spatial hierarchy: Site → Building → Storey → Space
  - Extracts property sets: `Pset_*`, `PSet_Revit_*`
  - Supports both IFC2x3 and IFC4 schemas
  - Graceful error handling for missing properties
  - Logging for extraction warnings and statistics

- **Data Export Formats**
  - `assets.csv`: All assets with flattened properties (785 rows × 327 columns)
  - `spatial_hierarchy.json`: Site → Building → Storey → Space relationships
  - `summary.json`: Statistics including asset counts and property sets extracted

- **Test Data Validation**
  - **Duplex Apartment (IFC2x3):** 785 assets extracted
  - **PCERT Sample Scene (IFC4):** 49 assets extracted
  - Confirmed compatibility with both IFC versions

---

#### Documentation

- **Architecture Decision Records (ADRs)**
  - ADR 0001: Use IfcOpenShell for IFC Parsing
  - ADR 0002: Use PostgreSQL (Supabase) for Storage
  - ADR 0003: Use Supabase over Local Docker
  - ADR 0004: IFC Extraction Approach — Phase 1
  - ADR 0005: Use Environment Variables for Secrets

- **Software Requirements Specification** (`docs/srs.md`)
  - Complete requirements for all 5 functional areas (FR-01 to FR-05)
  - Non-functional requirements (performance, maintainability, data quality)
  - Technology stack documentation
  - Milestones and roadmap
  - Risk assessment and mitigations

- **Project Documentation**
  - README with setup instructions and project overview
  - CHANGELOG (this file)
  - `.gitignore` for Python, IDE, and data files
  - `requirements.txt` for dependency management
  - `pyproject.toml` for project metadata

---

#### Project Setup

- Git repository initialized
- Python virtual environment (venv)
- Folder structure:

```text
sbaip/
├── docs/                  # ADRs, SRS, CHANGELOG
├── src/
│   └── extract/           # IFC parser
├── data/
│   ├── raw/               # Original IFC files
│   └── processed/         # CSV, JSON outputs
├── tests/                 # Unit tests (future)
└── docker/                # Docker configuration (future)
```

---

### Results

| Metric | Value |
|----------|----------|
| **Total Assets Extracted** | 785 |
| **Asset Types** | 15 IFC classes |
| **Properties Extracted** | 327 columns |
| **Storeys** | 4 |
| **Spaces** | 21 |
| **IFC Files Processed** | 2 (IFC2x3 + IFC4) |

#### Asset Breakdown

| Asset Type | Count |
|----------|----------|
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

### Technical Details

| Aspect | Details |
|----------|----------|
| **Python Version** | 3.14.2 |
| **Key Libraries** | IfcOpenShell 0.7+, pandas 2.0+, numpy 1.24+ |
| **IFC Versions** | IFC2x3 (primary), IFC4 (validated) |
| **Data Formats** | CSV, JSON, SQL (planned) |
| **Database** | Supabase (PostgreSQL) — decided, not yet implemented |

---

### Known Issues

- **MEP Assets Not Extracted**  
  The Duplex Apartment architectural model does not contain MEP (Mechanical, Electrical, Plumbing) assets. MEP extraction is planned for Phase 2 using `Duplex_MEP_20110907.ifc`.

- **Property Value Truncation**  
  Property values are truncated at 500 characters for CSV compatibility. Full values are preserved in the `asset_properties` table when loaded to PostgreSQL.

- **IFC4 Schema Differences**  
  Some IFC4 classes (e.g., `IfcElectricalElement`) are not present in IFC2x3. The script handles this gracefully with warnings.

- **Performance**  
  Parsing very large IFC files (>100MB) may be slower. Optimization is planned for future releases.

---

### Lessons Learned

1. **IFC Version Differences**  
   IFC2x3 and IFC4 have different class names and schemas. The script must handle both with fallbacks.

2. **Vendor-Specific Property Sets**  
   Revit exports include `PSet_Revit_*` property sets. These contain valuable operational data (e.g., circuit numbers, installation dates) that should be preserved.

3. **Data Variability**  
   Property values vary widely (numbers, strings, lists, empty values). Robust type handling is essential.

4. **Resource Constraints**  
   Local resources (RAM, storage) are limited. Cloud-hosted solutions (Supabase) reduce local resource consumption.

5. **Documentation**  
   ADRs and SRS are essential for project clarity, especially when the project will be showcased for jobs, scholarships, or funding applications.

---

### Next Steps (Phase 2: Database + Load)

- Set up Supabase project
- Create database schema (`src/load/db_schema.sql`)
- Load 785 assets into PostgreSQL
- Validate data with SQL queries
- Update documentation with Phase 2 results

---

## [Unreleased] — Next Phase

### Planned for v0.2.0 (Database + Load)

- Set up Supabase project and PostgreSQL schema
- Load 785 assets into the database
- Create a simple Streamlit dashboard to visualize the first five assets
- **First Validation Query:** "Which room is overheating?"
- **Scalability Test:** Load 10,000 virtual assets to validate performance

### Planned for v0.3.0 (Sensor Simulator)

- Temperature sensor simulation (18–26°C)
- CO₂ sensor simulation (400–1200 ppm)
- Energy consumption simulation (kWh)
- MQTT/Kafka output integration
- Schedule with Airflow

### Planned for v0.4.0 (REST API)

- FastAPI endpoints for assets, properties, locations
- OpenAPI documentation
- Integration with Supabase
- Authentication (future)

### Planned for v0.5.0 (Dashboard)

- Streamlit dashboard
- Building summary view
- Asset search and filter
- Asset detail view
- Alerts display
- 3D floor plan (future)

### Planned for v1.0.0 (Production Ready)

- CI/CD with GitHub Actions
- 80% test coverage
- Docker deployment
- AWS cloud migration
- Performance optimization
- Full documentation

---

## Versioning Scheme

| Version | Phase | Description |
|----------|----------|----------|
| 0.1.0 | Phase 1 | IFC Extraction Complete |
| 0.2.0 | Phase 2 | Database + Load |
| 0.3.0 | Phase 3 | Sensor Simulator |
| 0.4.0 | Phase 4 | REST API |
| 0.5.0 | Phase 5 | Dashboard |
| 1.0.0 | Phase 6 | Production Ready |

---

## References

- adr/0001-use-ifcopenshell-for-parsing.md
- adr/0002-use-postgresql-for-storage.md
- adr/0003-use-supabase-over-docker.md
- adr/0004-ifc-extraction-approach.md
- adr/0005-use-env-variables.md
- SRS
- https://www.buildingsmart.org/standards/
- https://supabase.com/docs

---

## About

SBAIP (Smart Building Asset Intelligence Platform) is a personal project by **Uchechukwu Obi** to demonstrate BIM-to-Digital-Twin data engineering skills for:

- 🔬 **Research:** Conference papers and academic presentations
- 💼 **Employment:** BIM Data Engineer, Digital Twin Engineer roles
- 🎓 **Education:** MSc portfolio and thesis foundation
- 💰 **Funding:** Scholarship and grant applications

---

## License

MIT License — see LICENSE for details.

---

## Author

**Uchechukwu Obi**

- GitHub: https://github.com/uchechukwuobi
- LinkedIn: https://linkedin.com/in/uchechukwuobi

---

*This changelog follows https://keepachangelog.com/ conventions and semantic versioning https://semver.org/.*