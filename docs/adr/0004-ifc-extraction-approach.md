# ADR 0004: IFC Extraction Approach — Phase 1

## Status
Completed — 2026-08-09

## Context
Phase 1 of SBAIP requires extracting structured asset data from IFC files. The extraction must:
- Support IFC2x3 (widely available)
- Support IFC4 (modern standard)
- Extract architectural elements (walls, doors, windows, slabs, etc.)
- Extract spatial hierarchy (site, building, storey, space)
- Extract property sets (Pset_*, PSet_Revit_*)
- Output CSV, JSON, and SQL-ready data

## Decision Drivers
- **Completeness:** Must extract all relevant asset data
- **Compatibility:** Must work with both IFC2x3 and IFC4
- **Extensibility:** Must allow future extraction of MEP elements
- **Performance:** Must handle files up to 100MB
- **Maintainability:** Code must be clear and documented

## Decision
Approach:
1. Use `IfcOpenShell` for IFC parsing (see ADR 0001)
2. Extract all products by type (IfcWall, IfcDoor, IfcSpace, etc.)
3. Extract spatial hierarchy (IfcSite → IfcBuilding → IfcBuildingStorey → IfcSpace)
4. Extract property sets (Pset_*, PSet_Revit_*)
5. Output to CSV, JSON, and PostgreSQL-ready format

## Results

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

## Implementation Notes
- Script: `src/extract/ifc_parser.py`
- Library: IfcOpenShell (Python)
- Output: `data/processed/assets.csv`, `spatial_hierarchy.json`, `summary.json`

## Known Issues
- MEP assets not extracted (planned for Phase 2)
- Property values truncated at 500 characters for CSV
- IFC4 schema differences handled with warnings

## References
- [ADR 0001](0001-use-ifcopenshell-for-parsing.md) — IfcOpenShell Decision
- [SRS](SRS.md) — FR-01: IFC Parsing

## Date
2026-08-09