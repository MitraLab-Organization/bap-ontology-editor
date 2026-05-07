#!/usr/bin/env python3
"""
Convert marmosetlist.csv to marmoset_brain.yaml nomenclature file.

Uses the marmoset species ID range (BAP_1XXXXXX) to fit within the
bootstrapped species ontology. The Brain node is created under Head
(BAP_1000001) following the same pattern as body_regions.yaml, and
all marmoset atlas structures are placed under it.
"""

import csv
import re
from datetime import date

CSV_PATH = "marmosetlist.csv"
OUTPUT_PATH = "structures/brain.yaml"

HEAD_ID = "BAP_1000001"
BRAIN_ID = "BAP_1010000"
ID_OFFSET = 1010000


def make_bap_id(region_id: int) -> str:
    return f"BAP_{ID_OFFSET + region_id:07d}"


def main():
    rows = []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    header = f"""metadata:
  category: brain
  description: Marmoset brain nomenclature (Brain/MINDS Marmoset Brain Atlas)
  version: 1.0.0
  last_modified: '{date.today().isoformat()}'
  source: marmosetlist.csv
  species: Callithrix jacchus
  ncbi_taxon: '9483'
structures:
- id: {BRAIN_ID}
  name: Brain
  parent: {HEAD_ID}
  definition: Central nervous system organ of the marmoset head

"""

    entries = []
    for row in rows:
        rid = int(row["RegionID"])
        pid = int(row["ParentID"])
        name = re.sub(r'[^\x20-\x7E]', ' ', row["Region"]).strip()
        name = re.sub(r' {2,}', ' ', name)
        acronym = row["RegionAcronym"].strip()

        bap_id = make_bap_id(rid)

        if rid == 1:
            parent = BRAIN_ID
        else:
            parent = make_bap_id(pid)

        color_parts = []
        for c in ["Color_1", "Color_2", "Color_3"]:
            val = row.get(c, "").strip()
            if val:
                color_parts.append(val)

        entry = f"- id: {bap_id}\n"
        entry += f"  name: {name}\n"
        entry += f"  parent: {parent}\n"
        entry += f"  abbreviation: '{acronym}'\n"
        entry += f"  xref: MARMOSET:{rid}\n"

        if len(color_parts) == 3:
            r_val = round(float(color_parts[0]) * 255)
            g_val = round(float(color_parts[1]) * 255)
            b_val = round(float(color_parts[2]) * 255)
            entry += f"  color_rgb: '{r_val},{g_val},{b_val}'\n"

        entries.append(entry)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(header)
        f.write("\n".join(entries))
        f.write("\n")

    print(f"Generated {OUTPUT_PATH} with {len(entries) + 1} structures (incl. Brain node)")


if __name__ == "__main__":
    main()
