import requests
from bs4 import BeautifulSoup
import json

url = 'https://mgkct.minskedu.gov.by/%D0%BE-%D0%BA%D0%BE%D0%BB%D0%BB%D0%B5%D0%B4%D0%B6%D0%B5/%D0%BF%D0%B5%D0%B4%D0%B0%D0%B3%D0%BE%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9-%D0%BA%D0%BE%D0%BB%D0%BB%D0%B5%D0%BA%D1%82%D0%B8%D0%B2'

response = requests.get(url)

if response.status_code != 200:
    print(f"Ошибка: {response.status_code}")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

info = soup.findAll("div", class_ = "content taj")
teachers_data = []

for data in info:
    teachers_names_tag = data.select_one("h3")
    teacher_name = teachers_names_tag.get_text(strip=True) if teachers_names_tag else "No teacher"

    teachers_posts_tag = data.select_one("li", class_ = "tss")
    teacher_post = teachers_posts_tag.get_text(strip = True) if teachers_posts_tag else "No post"

    teachers_data.append({"Teacher": teacher_name, "Post": teacher_post})

for i, teacher in enumerate(teachers_data, start = 1):
    print(f"{i}. Преподователь: {teacher['Teacher']}; {teacher['Post']};")

with open('data.json', 'w', encoding = 'utf-8') as file:
    json.dump(teachers_data, file, indent = 4, ensure_ascii = False)

with open('data.json', 'r', encoding = 'utf-8') as file:
    data = json.load(file)


with open('data.json', 'r', encoding = 'utf-8') as file:
    data = json.load(file)


html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Информация о преподователях</title>
    <style>
        body {{
            background-color: #d4eec6;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #000000;
        }}
        th {{
            background-color: #2ba732;
            color: white;
        }}
    </style>
</head>
<body>
    <h1>Информация о преподователях</h1>
    <table>
        <tr>
            <th>Преподователь</th>
            <th>Должность</th>
        </tr>
        {''.join(f"<tr><td>{teacher['Teacher']}</td><td>{teacher['Post']}</td></tr>" for teacher in data)}
    </table>
    <p>Ссылка на источник: <a href = 'https://mgkct.minskedu.gov.by/%D0%BE-%D0%BA%D0%BE%D0%BB%D0%BB%D0%B5%D0%B4%D0%B6%D0%B5/%D0%BF%D0%B5%D0%B4%D0%B0%D0%B3%D0%BE%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9-%D0%BA%D0%BE%D0%BB%D0%BB%D0%B5%D0%BA%D1%82%D0%B8%D0%B2'>Минский государственный колледж цифровых технологий</a></p>
</body>
</html>
"""


with open('index.html', 'w', encoding='utf-8') as file:
    file.write(html_content)
