from pathlib import Path
import re

filename = 'halstead_values.txt'

file_path = Path(filename)

# Read the file
with open(file_path, 'r') as file:
        content = file.read()

# Round float values to two decimals
content = re.sub(r'(\d+\.\d+)', lambda match: str(round(float(match.group(0)), 2)), content)

# Write the updated values back to the file
new_file = Path(file_path.stem + '2' + file_path.suffix)

with open(new_file, 'w') as file:
        file.write(content)
