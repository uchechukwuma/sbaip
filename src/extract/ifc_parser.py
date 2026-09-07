"""
IFC Asset Extraction Module
Extracts building assets, properties, and spatial hierarchy from an IFC file.
"""

import ifcopenshell
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class IFCParser:
    """Parser for extracting structured data from IFC files."""
    
    def __init__(self, file_path: str):
        """
        Initialize parser with IFC file path.
        
        Args:
            file_path: Path to .ifc file
        """
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"IFC file not found: {file_path}")
        
        self.model = ifcopenshell.open(str(self.file_path))
        logger.info(f"Loaded IFC file: {self.file_path.name} ({len(self.model.by_type('IfcProduct'))} products)")
        
        self.assets = []
        self.spatial_hierarchy = {}
        self.property_sets = []
        
    def extract_products(self, product_type: str = "IfcElement") -> List[Dict]:
        """
        Extract all products of a given type.
        
        Args:
            product_type: IFC class name (e.g., 'IfcDoor', 'IfcWall', 'IfcElement')
            
        Returns:
            List of dictionaries with product data
        """
        products = self.model.by_type(product_type)
        extracted = []
        
        for product in products:
            data = {
                "GlobalId": getattr(product, "GlobalId", None),
                "Name": getattr(product, "Name", None),
                "Description": getattr(product, "Description", None),
                "ObjectType": getattr(product, "ObjectType", None),
                "Type": product_type,
                "Storey": self._get_storey(product),
                "Space": self._get_space(product),
                "Properties": self._get_properties(product),
            }
            extracted.append(data)
        
        logger.info(f"Extracted {len(extracted)} {product_type} objects")
        return extracted
    
    def extract_all_elements(self) -> List[Dict]:
        """
        Extract all building elements including architectural, structural, and MEP.
        """
        element_types = [
            # Architectural
            "IfcWall", "IfcWallStandardCase",
            "IfcDoor", "IfcWindow",
            "IfcSlab", "IfcRoof",
            "IfcColumn", "IfcBeam",
            "IfcStair", "IfcRamp",
            "IfcSpace", "IfcBuildingStorey", "IfcBuilding",
            "IfcCovering", "IfcCurtainWall",
            
            # MEP (Mechanical, Electrical, Plumbing)
            "IfcFlowMovingDevice",      # Fans, pumps
            "IfcFlowTerminal",          # Diffusers, grilles
            "IfcFlowSegment",           # Ducts, pipes
            "IfcFlowFitting",           # Elbows, tees
            "IfcFlowController",        # Valves, dampers
            "IfcFlowTreatmentDevice",   # Filters, coils
            "IfcElectricalElement",
            "IfcLightFixture",
            "IfcLamp",
            "IfcCableCarrierFitting",
            "IfcCableCarrierSegment",
            
            # Generic fallback
            "IfcElement",
            "IfcProduct",
        ]
        
        all_elements = []
        for elem_type in element_types:
            try:
                elements = self.extract_products(elem_type)
                all_elements.extend(elements)
            except Exception as e:
                logger.warning(f"Could not extract {elem_type}: {e}")
        
        logger.info(f"Total elements extracted: {len(all_elements)}")
        return all_elements
    
    def extract_spatial_hierarchy(self) -> Dict:
        """Extract the spatial hierarchy: Site → Building → Storey → Space."""
        hierarchy = {
            "sites": [],
            "buildings": [],
            "storeys": [],
            "spaces": []
        }
        
        # Sites
        sites = self.model.by_type("IfcSite")
        for site in sites:
            hierarchy["sites"].append({
                "GlobalId": site.GlobalId,
                "Name": site.Name,
                "LongName": getattr(site, "LongName", None)
            })
        
        # Buildings
        buildings = self.model.by_type("IfcBuilding")
        for building in buildings:
            hierarchy["buildings"].append({
                "GlobalId": building.GlobalId,
                "Name": building.Name,
                "LongName": getattr(building, "LongName", None)
            })
        
        # Storeys
        storeys = self.model.by_type("IfcBuildingStorey")
        for storey in storeys:
            hierarchy["storeys"].append({
                "GlobalId": storey.GlobalId,
                "Name": storey.Name,
                "Elevation": getattr(storey, "Elevation", None)
            })
        
        # Spaces
        spaces = self.model.by_type("IfcSpace")
        for space in spaces:
            hierarchy["spaces"].append({
                "GlobalId": space.GlobalId,
                "Name": space.Name,
                "LongName": getattr(space, "LongName", None)
            })
        
        logger.info(f"Spatial hierarchy: {len(hierarchy['sites'])} sites, {len(hierarchy['buildings'])} buildings, "
                   f"{len(hierarchy['storeys'])} storeys, {len(hierarchy['spaces'])} spaces")
        return hierarchy
    
    def extract_property_sets(self, product) -> Dict:
        """Extract all property sets from a product."""
        props = {}
        if hasattr(product, "IsDefinedBy"):
            for rel in product.IsDefinedBy:
                if rel.is_a("IfcRelDefinesByProperties"):
                    prop_set = rel.RelatingPropertyDefinition
                    if prop_set.is_a("IfcPropertySet"):
                        set_name = prop_set.Name
                        props[set_name] = {}
                        for prop in prop_set.HasProperties:
                            prop_name = prop.Name
                            if prop.is_a("IfcPropertySingleValue"):
                                value = prop.NominalValue.wrappedValue if prop.NominalValue else None
                                props[set_name][prop_name] = value
                            elif prop.is_a("IfcPropertyEnumeratedValue"):
                                values = prop.EnumerationValues
                                if values:
                                    props[set_name][prop_name] = [v.wrappedValue for v in values if v]
        return props
    
    def _get_storey(self, product) -> Optional[str]:
        """Get the storey name for a product."""
        try:
            if hasattr(product, "ContainedInStructure"):
                for rel in product.ContainedInStructure:
                    if rel.is_a("IfcRelContainedInSpatialStructure"):
                        container = rel.RelatingStructure
                        if container.is_a("IfcBuildingStorey"):
                            return container.Name
        except:
            pass
        return None
    
    def _get_space(self, product) -> Optional[str]:
        """Get the space name for a product."""
        try:
            if hasattr(product, "ContainedInStructure"):
                for rel in product.ContainedInStructure:
                    if rel.is_a("IfcRelContainedInSpatialStructure"):
                        container = rel.RelatingStructure
                        if container.is_a("IfcSpace"):
                            return container.Name
        except:
            pass
        return None
    
    def _get_properties(self, product) -> Dict:
        """Get all property sets for a product."""
        return self.extract_property_sets(product)
    
    def to_dataframe(self, elements: List[Dict]) -> pd.DataFrame:
        """Convert extracted elements to a pandas DataFrame."""
        rows = []
        for elem in elements:
            row = {
                "global_id": elem["GlobalId"],
                "name": elem["Name"],
                "type": elem["Type"],
                "object_type": elem["ObjectType"],
                "storey": elem["Storey"],
                "space": elem["Space"],
            }
            # Properties added as flattened columns
            for pset_name, props in elem["Properties"].items():
                for prop_name, value in props.items():
                    if value is not None:
                        col_name = f"{pset_name}_{prop_name}".replace(" ", "_")
                        # Converts lists to strings for CSV
                        if isinstance(value, list):
                            value = ", ".join(str(v) for v in value)
                        row[col_name] = str(value)[:500]  # Truncate long values
            
            rows.append(row)
        
        return pd.DataFrame(rows)
    
    def save_output(self, elements: List[Dict], output_dir: str = "data/processed"):
        """
        Save extracted data to CSV and JSON files.
        
        Args:
            elements: List of extracted element dictionaries
            output_dir: Directory to save output files
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save as CSV
        df = self.to_dataframe(elements)
        csv_path = output_path / "assets.csv"
        df.to_csv(csv_path, index=False)
        logger.info(f"Saved {len(df)} assets to {csv_path}")
        
        # Save hierarchy as JSON
        hierarchy = self.extract_spatial_hierarchy()
        json_path = output_path / "spatial_hierarchy.json"
        with open(json_path, "w") as f:
            json.dump(hierarchy, f, indent=2, default=str)
        logger.info(f"Saved spatial hierarchy to {json_path}")
        
        # Save summary statistics
        summary = {
            "total_assets": len(elements),
            "asset_types": df["type"].value_counts().to_dict() if "type" in df.columns else {},
            "total_storeys": len(hierarchy["storeys"]),
            "total_spaces": len(hierarchy["spaces"]),
            "file_name": self.file_path.name,
            "properties_extracted": list(df.columns) if not df.empty else [],
        }
        summary_path = output_path / "summary.json"
        with open(summary_path, "w") as f:
            json.dump(summary, f, indent=2)
        logger.info(f"Saved summary to {summary_path}")
        
        return df
    
    def get_asset_by_global_id(self, global_id: str) -> Optional[Dict]:
        """Find an asset by its GlobalId."""
        product = self.model.by_guid(global_id)
        if product:
            return {
                "GlobalId": product.GlobalId,
                "Name": product.Name,
                "Type": product.is_a(),
                "Storey": self._get_storey(product),
                "Space": self._get_space(product),
                "Properties": self._get_properties(product),
            }
        return None


def main():
    """Main execution function."""
    # Path to IFC file
    ifc_file = "data/raw/Duplex_A_20110907.ifc"
    
    # Initialize parser
    parser = IFCParser(ifc_file)
    
    # Extract all elements
    elements = parser.extract_all_elements()
    
    # Save output
    df = parser.save_output(elements, "data/processed")
    
    # Print summary
    print("\n" + "="*50)
    print("EXTRACTION SUMMARY")
    print("="*50)
    print(f"Total assets extracted: {len(df)}")
    print(f"Asset types: {df['type'].value_counts().to_dict() if 'type' in df.columns else 'N/A'}")
    print(f"Columns extracted: {len(df.columns)}")
    print(f"Output saved to: data/processed/")
    print("="*50)
    print("\nFiles created:")
    print("  - data/processed/assets.csv")
    print("  - data/processed/spatial_hierarchy.json")
    print("  - data/processed/summary.json")
    print("="*50 + "\n")
    
    return df


if __name__ == "__main__":
    main()