import re
from pathlib import Path


def file2array(filename):
    with open(filename, 'r', encoding='cp866') as f:
        keys = f.read().strip().splitlines()

    data = []
    line_number = 0
    for _, line in enumerate(keys[1:], start=1):
        if line.strip() and re.match(r'^\d', line):
            line_number += 1
            ex = line.split(';')
            entry = {f'line{j + 1}': ex[j] if j < len(ex) else '' for j in range(12)}
            # entry['line10'] = '01' if len(ex) > 4 and ex[4].strip() else '26'
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
partial_name = 'продаж'

for file in folder_path.iterdir():
    if file.is_file() and partial_name in file.name:
        print(file.resolve())
        break

data = file2array(file.resolve())

# Read XML template files
with open('tpl/prod_tpl_511.xml', 'r', encoding='cp1251') as f:
    base = f.read()
with open('tpl/prod_tpl1.xml', 'r', encoding='cp1251') as f:
    tpl = f.read()
with open('tpl/prod_tpl2.xml', 'r', encoding='cp1251') as f:
    tpl_ind_pred = f.read()
with open('tpl/prod_tpl3.xml', 'r', encoding='cp1251') as f:
    tpl_ext = f.read()
with open('tpl/prod_tpl4.xml', 'r', encoding='cp1251') as f:
    tpl_26 = f.read()
with open('tpl/prod_tpl5.xml', 'r', encoding='cp1251') as f:
    tpl_02 = f.read()

text = ''
sum8 = 0
sum9 = 0

# Dictionary for INN corrections
inn_corrections = {
    '47120521290': '471205212902',
    '266066722': '0266066722',
    '274191036': '0274191036',
    '326016895': '0326016895',
    '276126850': '0276126850',
    '274062111': '0274062111',
    '274907739': '0274907739',
    '276935139': '0276935139',
    '2682483545': '02682483545'
}


# Process data
for element in data:
    if not element["line2"].strip():
        break

    inn = element["line5"].strip()
    inn = inn_corrections.get(inn, inn)

    if len(inn) in [9, 11]:
        inn = '0' + inn

    if len(inn) == 12:
        tmp_tpl = tpl_ind_pred
    elif element["line10"] == '18':
        tmp_tpl = tpl_ext
    elif element["line10"] == '26':
        tmp_tpl = tpl_26
    elif element["line10"] == '02':
        tmp_tpl = tpl_02
    else:
        tmp_tpl = tpl

    fill = tmp_tpl.replace('$line10', element["line10"])
    fill = fill.replace('$line1', clear(element["line1"]))
    fill = fill.replace('$line2', element["line2"].strip())
    fill = fill.replace('$line3', element["line3"])
    fill = fill.replace('$line4', element["line4"])
    fill = fill.replace('$line5', inn)
    kpp = clear(element["line6"])
    if len(kpp) == 8:
        kpp = "0" + kpp
    fill = fill.replace('$line6', kpp)
    fill = fill.replace('$line7', clear(element["line7"]))
    fill = fill.replace('$line8', clear(element["line8"]))
    tmp8 = clear(element["line8"])
    fill = fill.replace('$line9', clear(element["line9"]))
    tmp9 = clear(element["line9"])

    if element["line10"] == '18':
        fill = fill.replace('$line_11', element["line11"].strip())
        fill = fill.replace('$line_12', element["line12"].strip())

    text += fill
    if tmp8.strip():
        sum8 += float(tmp8)
    if tmp9.strip():
        sum9 += float(tmp9)


# Final processing
base = base.replace('$data', text)
base = base.replace('$sum8', str(round(sum8, 2)))
base = base.replace('$sum9', str(round(sum9, 2)))

# Write to output file

folder_path = Path('D:/prodaz')  # Use forward slashes or raw string
folder_path.mkdir(parents=True, exist_ok=True)

file_name = 'NO_NDS.9_7801_7801_780161151018_20250726_375457CA-AD2B-47FF-A025-ABF337C26A36.xml'
out_path = folder_path / file_name
with open(str(out_path), 'w', encoding='cp1251') as f:
    f.write(base)

print("done")
