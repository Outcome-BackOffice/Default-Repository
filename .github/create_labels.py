import json
import os

import requests

# 환경 변수에서 GitHub 토큰 불러오기
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]

# labels.json 파일을 읽어서 레이블 생성
with open(".github/labels.json", "r", encoding="utf-8") as file:
    labels = json.load(file)

repo = "Outcome-BackOffice/test2"
url = f"https://api.github.com/repos/{repo}/labels"
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

for label in labels:
    response = requests.post(url, headers=headers, json=label)
    if response.status_code == 201:
        print(f"Label '{label['name']}' created successfully.")
    elif response.status_code == 422:
        print(f"Label '{label['name']}' already exists.")
    else:
        print(f"Failed to create label '{label['name']}': {response.content}")
