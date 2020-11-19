import pdfplumber
import re
import pickle
pdf = pdfplumber.open('data/plan1.pdf')
page = pdf.pages[0]
text = page.extract_text()
pdf.close()
pdf2 = pdfplumber.open('data/MKA2-SKE.pdf')
n = r'(?:ปีที่ ([0-9])   ภาคการศึกษาที่ ([0-9]))?[^0-9]+([0-9x]{8,9})  ([^0-9]+) ([0-9-\(\)]+)'
old = r'([0-9]{1,8})  (.+)  ([0-6-\(\)]+)'
last_year, last_sem = (1, 1)

try:
    d = pickle.load(open("data/big_file_dump", "rb"))
except:
    d = {}
    for i in range(33):
        page2 = pdf2.pages[i]
        text2 = page2.extract_text()
        for en_info in re.findall(r'([0-9*]{1,10}) {1,2}([^0-9]+) +([0-9-\n\(\)]+)[\u0E00-\u0E7F 0-9.\n]+\(([A-z ]+)\)', text2,
                                  flags=re.MULTILINE):
            d[en_info[0].replace("*", "")] = en_info[3].rstrip().replace("  ", " "), en_info[2]

    pickle.dump(d, open("data/big_file_dump", "wb"), protocol=pickle.HIGHEST_PROTOCOL)


with open('data/out.csv', 'w') as f:
    print("id,name_th,credits,name_en,year_start,semester", file=f)
    ld = []
    for i in range(3):
        page = pdf.pages[i]
        text = page.extract_text()
        for j in re.findall(n, text):
            name_en = d.get(j[2], "None")
            if j[0] != "" and j[1] != "":
                last_year, last_sem = j[0], j[1]
            j = list(j[2:])
            j[1] = j[1].replace(" ", "")
            j.extend([name_en[0], str(last_year), str(last_sem)])
            ld.append(','.join(j))

    print("\n".join(ld), file=f)
