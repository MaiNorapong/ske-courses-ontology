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
q = r'([0-9*]{1,10}) {1,2}([^0-9]+) +([0-9-\n\(\)]+)[\u0E00-\u0E7F 0-9.\n]+\(([A-z ]+)\)'
# r = r'([0-9*]{6,10}) +([^0-9]+) +([0-9-\n\(\)]+) [\u0E00-\u0E7F 0-9.\n]+\(([A-z ]+)\)[ \n]*(?:วชิ าทต่ี อ้ งเรยี นมาก่อน ([0-9]+))?([\n\u0E00-\u0E7F ]*) *([\nA-Za-z-.,:; ]*)'

r = r'([0-9*]{6,10}) +([^0-9]+) +([0-9-\n\(\)]+) [\u0E00-\u0E7F 0-9.\n]+\(([A-z ]+)\)[ \n]*(?:วชิ าทต่ี อ้ งเรยี นมาก่อน[ :]+([0-9\u0E00-\u0E7F, ]+))?[ \n]? +(?:(?:วชิ าทต่ี อ้ งเรยี นพรอ้ มกนั|วชิ าตอ้ งทเ่ี รยี นพรอ้ มกนั)[ :]+([0-9\u0E00-\u0E7F, ]+))?([0-9\n\u0E00-\u0E7F-/ ]*) *([/\nA-Za-z-.,:; \(\)]*)'

d = {}
# try:
#     d = pickle.load(open("data/big_file_dump", "rb"))
# except:
#     d = {}
#     for i in range(33):
#         page2 = pdf2.pages[i]
#         text2 = page2.extract_text()
#         # print(text2, file=open('data/dump.txt', 'a'))
#         for en_info in re.findall(r, text2,
#                                   flags=re.MULTILINE):
#             d[en_info[0].replace("*", "")] = en_info[3].rstrip().replace("  ", " "), en_info[2]
#
#     pickle.dump(d, open("data/big_file_dump", "wb"), protocol=pickle.HIGHEST_PROTOCOL)

t = open("data/dump.txt", "r").read()
for en_info in re.findall(r, t, flags=re.MULTILINE):
    prereq = en_info[4].rstrip().lstrip().replace(" และ ", ",")
    coreg = en_info[5].rstrip().lstrip()
    desc_th = en_info[6].rstrip().lstrip()
    desc_en = en_info[7].rstrip().lstrip()
    d[en_info[0].replace("*", "")] = en_info[3].rstrip().replace("  ", " "), en_info[2], prereq, coreg, desc_th, desc_en

with open('data/out.csv', 'w') as f:
    print("id,name_th,credits,name_en,year_start,semester,prereq,coreg,desc_th,desc_en", file=f)
    ld = []
    for i in range(3):
        page = pdf.pages[i]
        text = page.extract_text()
        for j in re.findall(n, text):
            extra = d.get(j[2], "None")
            if j[0] != "" and j[1] != "":
                last_year, last_sem = j[0], j[1]
            j = list(j[2:])
            j[1] = j[1].replace(" ", "")
            if isinstance(extra, tuple):
                j.extend([extra[0], str(last_year), str(last_sem), f'"{extra[2]}"', extra[3], f"\"{extra[4]}\"",
                          f"\"{extra[5]}\""])
            elif not isinstance(extra, str):
                j.extend(["N", str(last_year), str(last_sem), "N", "N", "N", "N"])
            ld.append(','.join(j))

    print("\n".join(ld), file=f)
