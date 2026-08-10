# ADR 0001: Use IfcOpenShell for IFC Parsing

## Status
Accepted — 2026-08-09

## Context
We need to extract asset data from IFC files (both IFC2x3 and IFC4) for the Smart Building Asset Intelligence Platform (SBAIP). The extraction must handle:
- Architectural elements (walls, doors, windows, slabs, roofs)
- Spatial hierarchy (site, building, storey, space)
- Property sets (Pset_*, PSet_Revit_*)
- MEP elements (HVAC, plumbing, electrical) — future

Options considered:
- IfcOpenShell (Python)
- Revit API (Windows-only, requires license)
- xBIM (C#, .NET)
- Commercial SDKs (costly)

## Decision Drivers
- Cost: Need a free, open-source solution
- Portability: Must work across platforms (Windows, Linux, macOS)
- Integration: Must work with Python data pipeline
- Standards: Must support IFC2x3 and IFC4

## Decision
Use IfcOpenShell (Python) because:
- Open source (MIT licensed)
- Cross-platform (Windows, Linux, macOS)
- Python ecosystem integration (Pandas, FastAPI)
- BuildingSMART compliant
- Free for commercial use
- Supports both IFC2x3 and IFC4
- Active community and documentation

## Consequences

### Positive
- Lower cost (free)
- Faster development (Python)
- Easy integration with data pipeline
- Portable across platforms

### Negative
- Performance may be slower for very large models (>500MB)
- Requires learning IFC schema concepts
- Limited geometry manipulation (not needed for this project)

## Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
| :--- | :--- | :--- | :--- |
| Revit API | Full Revit integration | Windows-only, license required | Not open, costly |
| xBIM | C# ecosystem | Requires .NET | Language mismatch |
| Commercial SDKs | Fully featured | Expensive, vendor lock-in | Budget constraints |

## Implementation Notes
- Script: `src/extract/ifc_parser.py`
- Extracted 785 assets from Duplex Apartment (IFC2x3)
- Extracted 49 assets from IFC4 sample (PCERT)
- Property sets extracted: Pset_WallCommon, Pset_DoorCommon, PSet_Revit_*

## References
- [IfcOpenShell Documentation](https://ifcopenshell.org/)
- [buildingSMART IFC Standards](https://www.buildingsmart.org/standards/)
- [IFC Schema Documentation](https://standards.buildingsmart.org/IFC/DEV/IFC4_2/FINAL/HTML/)

## Date
2026-08-09