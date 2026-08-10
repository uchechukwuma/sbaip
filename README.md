# 🏗️ SBAIP — Smart Building Asset Intelligence Platform

**Extract structured asset data from IFC/BIM files and build the foundation for a digital twin.**

[![Python](https://img.shields.io/badge/Python-3.14%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![IFC](https://img.shields.io/badge/IFC-2x3%20%7C%204-important)](https://www.buildingsmart.org/)
[![Status](https://img.shields.io/badge/Status-Phase%201%20Complete-brightgreen)](https://github.com/uchechukwuobi/sbaip)

---

## 📖 Overview

**SBAIP** is a data engineering platform that extracts structured asset data from IFC/BIM files and prepares it for a living digital twin.

### The Problem

Facility managers have information spread across BIM models, Excel sheets, maintenance logs, and sensor systems with no single place to answer questions like:

- *Where is AHU-03 located?*
- *When was it installed?*
- *Is it consuming too much energy?*
- *Is maintenance due?*

### Our Solution

A cloud-based platform that transforms a Building Information Model (IFC) into a structured asset repository, ready for integration with IoT sensor data, analytics, and dashboards.

---

## 🤔 Why This Project Exists

This project bridges the gap between **BIM (design phase)** and **facility management (operations phase)**. It is the foundation for answering questions that currently require manual searches across emails, PDFs, and spreadsheets. This platform is the first step toward a fully connected digital twin.

## 🎯 Current Status

| Phase | Focus | Status |
|---------|---------|---------|
| **Phase 1** | IFC Extraction (IFC2x3 & IFC4) | ✅ Complete |
| **Phase 2** | Database + Load (Supabase) | 🔄 In Progress |
| **Phase 3** | Sensor Simulator | 📋 Planned |
| **Phase 4** | REST API (FastAPI) | 📋 Planned |
| **Phase 5** | Dashboard (Streamlit) | 📋 Planned |
| **Phase 6** | Production Ready | 📋 Planned |

---

## 📊 Phase 1 Results

| Metric | Value |
|---------|---------|
| **Total Assets Extracted** | 785 |
| **Asset Types** | 15 IFC classes |
| **Properties Extracted** | 327 columns |
| **Storeys** | 4 |
| **Spaces** | 21 |
| **IFC Versions** | IFC2x3 + IFC4 |

### Asset Breakdown

| Asset Type | Count |
|---------|---------|
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

## 🛠️ Technology Stack

| Layer | Technology | Status |
|---------|---------|---------|
| Data Extraction | Python + IfcOpenShell | ✅ |
| Database | Supabase (PostgreSQL) | 🔄 |
| API | FastAPI | 📋 |
| Dashboard | Streamlit | 📋 |
| Orchestration | Apache Airflow | 📋 (Reused from Edge DataOps) |
| Data Quality | Great Expectations | 📋 (Reused from Edge DataOps) |
| Version Control | Git + GitHub | ✅ |
| Documentation | Markdown + ADRs | ✅ |

---

## 🔜 Next Steps (Phase 2: Database + Load)

In the next phase, I will:

1. Set up a Supabase (PostgreSQL) database
2. Load the 785 extracted assets into the database
3. Design a flexible schema for building assets and properties
4. Write SQL queries to validate the data

This will transform the platform from a file-based extraction tool into a queryable asset repository, the foundation of a true digital twin.

---

## 📂 Project Structure

```text
sbaip/
├── data/
│   ├── raw/                       # Original IFC files
│   └── processed/                 # CSV, JSON outputs
├── docs/
│   ├── adr/                       # Architecture Decision Records
│   ├── SRS.md                     # Software Requirements Specification
│   └── CHANGELOG.md               # Project changelog
├── src/
│   └── extract/
│       └── ifc_parser.py          # IFC asset extraction script
├── .env.example                   # Environment variables template
├── .gitignore                     # Python + data files
├── README.md                      # This file
├── requirements.txt               # Python dependencies
└── pyproject.toml                 # Project metadata
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.14+
- An IFC file to test (sample files in `data/raw/`)

### Installation

```bash
# Clone the repository
git clone https://github.com/uchechukwuobi/sbaip.git
cd sbaip

# Create virtual environment
python -m venv venv

# Activate environment
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
```

### Run the IFC Parser

```bash
python src/extract/ifc_parser.py
```

### Output

- `data/processed/assets.csv` — All assets with properties
- `data/processed/spatial_hierarchy.json` — Spatial structure
- `data/processed/summary.json` — Extraction statistics

---

## 📚 Documentation

| Document | Description |
|---------|---------|
| SRS.md | Software Requirements Specification |
| CHANGELOG.md | Version history and roadmap |
| ADR 0001 | IFC Parsing Decision |
| ADR 0002 | Database Decision |
| ADR 0003 | Supabase Decision |

---

## 🧠 Architecture Decision Records

| ADR | Title | Status |
|---------|---------|---------|
| ADR 0001 | Use IfcOpenShell for IFC Parsing | ✅ Accepted |
| ADR 0002 | Use PostgreSQL (Supabase) for Storage | ✅ Accepted |
| ADR 0003 | Use Supabase over Local Docker | ✅ Accepted |
| ADR 0004 | IFC Extraction Approach — Phase 1 | ✅ Completed |
| ADR 0005 | Use Environment Variables for Secrets | ✅ Accepted |
| ADR 0006 | Use FastAPI for REST API | 🔲 Planned |
| ADR 0007 | Use Streamlit for Dashboard | 🔲 Planned |
| ADR 0008 | Deploy to AWS Cloud | 🔲 Planned |

---

## ⚠️ Known Issues

| Issue | Status | Mitigation |
|---------|---------|---------|
| MEP assets not extracted | Phase 2 | Use `Duplex_MEP_*.ifc` |
| Property values truncated at 500 chars | Known | Preserved in PostgreSQL |
| IFC4 schema differences | Handled | Graceful fallbacks in parser |
| Large IFC files (>100MB) may be slow | Optimization | Planned for v1.0.0 |

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## 👤 Author

**Uchechukwu Obi**

- GitHub: https://github.com/uchechukwuobi
- LinkedIn: https://linkedin.com/in/uchechukwuobi

---

## 🙏 Acknowledgments

- IfcOpenShell — IFC parsing library
- buildingSMART — IFC standards
- Supabase — PostgreSQL cloud hosting

---

## 📌 Related Projects

- **Edge DataOps Platform** — IoT data pipeline (reused for SBAIP)
- **Career Intelligence Dashboard** — Data engineering portfolio

---

## 📊 Project Status

| Phase | Status | Completion |
|---------|---------|---------|
| **Phase 1: IFC Extraction** | ✅ Complete | 100% |
| Phase 2: Database + Load | 🔲 In Progress | 0% |
| Phase 3: Sensor Simulator | 🔲 Planned | 0% |
| Phase 4: REST API | 🔲 Planned | 0% |
| Phase 5: Dashboard | 🔲 Planned | 0% |
| Phase 6: Production Ready | 🔲 Planned | 0% |

---
