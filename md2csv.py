# abt this code
# what it does: pulls metadata from markdown files and makes a csv with them. 
# note: getting metadata from md ==> csv directly proved difficult. turning the data into json format first and then csv solved the issues, though not elegantly. 
# expected (tested) script output:
# - metadata.json
# - directory.csv
# - [ ] "id" column is still duplicated, dunno why yet

import frontmatter
from pathlib import Path
import json
import csv

root = Path(".")
output_json = Path("metadata.json")

metadata_records = []

for folder in root.glob("_issue*"):
    if not folder.is_dir():
        continue
    for md_file in folder.rglob("*.md"):
        if "intro" in md_file.name.lower():
            continue

        try:
            post = frontmatter.load(md_file)
            record = post.metadata.copy()
            record["id"] = str(md_file.relative_to(root))  # ID is relative path
            metadata_records.append(record)
        except Exception as e:
            print(f"error reading {md_file}: {e}")

# outputs json with metadata
with output_json.open("w", encoding="utf-8") as f:
    json.dump(metadata_records, f, indent=2, ensure_ascii=False)

print(f"wrote {len(metadata_records)} records to metadata.json")


# json ==> csv
with open("metadata.json", encoding="utf-8") as f:
    records = json.load(f)

# grab unique fieldnames
all_keys = set()
for r in records:
    all_keys.update(r.keys())

fieldnames = ["id"] + sorted(k for k in all_keys if k != "id")

with open("directory.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id"] + fieldnames)
    writer.writeheader()

    for r in records:
        row = {}
        for key in ["id"] + fieldnames:
            val = r.get(key, "")
            if isinstance(val, list):
                val = ", ".join(map(str, val))
            row[key] = val
        writer.writerow(row)

print("csv export complete.")