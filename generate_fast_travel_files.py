import os
import xml.etree.ElementTree as ET
import json
import math

# Paths (run from within 'livonia')
CUSTOM_DIR = 'custom'
XML_FILE = 'mapgrouppos.xml'
CFG_FILE = 'cfggameplay.json'

os.makedirs(CUSTOM_DIR, exist_ok=True)

tree = ET.parse(XML_FILE)
root = tree.getroot()

safe_positions = [
    [6193.794921875, 308.14166259765625, 6129.7197265625],
    [6187.9697265625, 308.14166259765625, 6129.6064453125],
    [6200.2880859375, 308.14166259765625, 6129.3056640625],
    [6180.5419921875, 308.14166259765625, 6130.37890625],
    [6174.14453125, 308.1416931152344, 6130.59765625]
]

# Collect new file paths to add to cfggameplay.json
new_files = []

for group in root.findall('group'):
    if group.attrib.get('name') == 'Land_Misc_Toilet_Dry':
        pos = group.attrib['pos']
        x, y, z = map(float, pos.split())
        x_f, z_f = math.floor(x), math.floor(z)
        coords = [x, y, z]
        area_name = f"fast-travel-{x_f}-{z_f}"
        filename = f"{CUSTOM_DIR}/fast-travel-{x_f}-{z_f}.json"
        rel_filename = f"./custom/fast-travel-{x_f}-{z_f}.json"
        if not os.path.exists(filename):
            data = {
                "areaName": area_name,
                "PRABoxes": [
                    [
                        [2, 3, 2],
                        [90, 0, 0],
                        coords
                    ]
                ],
                "safePositions3D": safe_positions
            }
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            new_files.append(rel_filename)

# Update cfggameplay.json
if new_files:
    with open(CFG_FILE, 'r') as f:
        cfg = json.load(f)
    prafiles = cfg.get('WorldsData', {}).get('playerRestrictedAreaFiles', [])
    for nf in new_files:
        if nf not in prafiles:
            prafiles.append(nf)
    cfg['WorldsData']['playerRestrictedAreaFiles'] = prafiles
    with open(CFG_FILE, 'w') as f:
        json.dump(cfg, f, indent=1)