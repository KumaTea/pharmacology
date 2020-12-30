import os
import csv


drugs_csv = './drugs.csv'
drugs_zh_csv = './drugs-zh.csv'

drugs_md_head = """# Drug Stems Cheat Sheet

Source: [NursesLabs](https://nurseslabs.com/common-generic-drug-stem-cheat-sheet/) (edited)

License: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

---

"""

drugs_zh_md_head = """# 药物速查表

来源: [NursesLabs](https://nurseslabs.com/common-generic-drug-stem-cheat-sheet/) (有删改)

License: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

---

"""


def generate_markdown(file, md_head):
    tmp = []
    with open(file, encoding=('utf-8' if 'zh' in file else 'gbk'), newline='') as f:
        content = csv.reader(f)
        # next(content)
        for row in content:
            tmp.append(row)
    first_line = tmp[0]
    tmp = tmp[1:]
    md_body = '| ' + ' | '.join(first_line) + ' |' + '\n'
    md_body += '|' + len(first_line)*' :---: |' + '\n'
    for j in tmp:
        md_body += '| ' + ' | '.join(j) + ' |' + '\n'
    with open(f'{file.replace("csv", "md")}', 'w', encoding='utf-8') as f:
        f.write(md_head + md_body)


if __name__ == '__main__':
    generate_markdown(drugs_csv, drugs_md_head)
    generate_markdown(drugs_zh_csv, drugs_zh_md_head)
