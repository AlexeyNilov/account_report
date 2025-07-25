import re
from pathlib import Path


def file2array(filename):
    with open(filename, 'r', encoding='cp866') as f:
        keys = f.read().strip().splitlines()

    data = []
    line_number = 0
    for i, line in enumerate(keys[1:], start=1):
        if line.strip():
            line_number += 1
            ex = line.split(';')
            entry = {f'line{j + 1}': ex[j] if j < len(ex) else '' for j in range(12)}
            entry['line1'] = str(line_number)
            data.append(entry)

    return data


# Function to clear input data
def clear(s):
    s = s.strip()
    s = s.replace(',', '.')
    s = re.sub(r'[^\d.]', '', s)
    return s


# Read input CSV data

folder_path = Path('D:')
partial_name = 'покупок'

for file in folder_path.iterdir():
    if file.is_file() and partial_name in file.name:
        print(file.resolve())

data = file2array(file.resolve())

# Read XML template files
with open('tpl/pok_tpl_511.xml', 'r', encoding='cp1251') as f:
    base = f.read()
with open('tpl/pok_tpl1.xml', 'r', encoding='cp1251') as f:
    tpl = f.read()

text = ''
sum8 = 0

# Process data
for element in data:
    if not element["line2"].strip():
        break
    fill = tpl.replace('$line10', element["line10"])
    fill = fill.replace('$line1', clear(element["line1"]))
    fill = fill.replace('$line2', element["line2"].strip())
    fill = fill.replace('$line3', element["line3"])
    fill = fill.replace('$line4', element["line4"])
    fill = fill.replace('$line5', element["line5"])
    fill = fill.replace('$line6', element["line6"])
    fill = fill.replace('$line7', clear(element["line7"]))
    fill = fill.replace('$line8', clear(element["line8"]))
    tmp8 = clear(element["line8"])
    fill = fill.replace('$line9', clear(element["line9"]))

    text += fill
    if tmp8.strip():
        sum8 += float(tmp8)


# Final processing
base = base.replace('$data', text)
base = base.replace('$sum8', str(round(sum8, 2)))

# Write to output file
folder_path = Path('D:/pokupok')  # Use forward slashes or raw string
folder_path.mkdir(parents=True, exist_ok=True)

file_name = 'NO_NDS.8_7801_7801_780161151018_20250425_FCD6C7D8-F17B-4C17-AA1B-9AA07BA762AE.xml'
out_path = folder_path / file_name
with open(str(out_path), 'w', encoding='cp1251') as f:
    f.write(base)

print("done")
