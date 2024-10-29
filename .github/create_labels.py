import json
import os

import requests

# 환경 변수에서 현재 레포지토리 이름과 GitHub 토큰 가져오기
repo = os.environ["GITHUB_REPOSITORY"]
url = f"https://api.github.com/repos/{repo}/labels"
headers = {
    "Authorization": f"token {os.environ['GITHUB_TOKEN']}",
    "Accept": "application/vnd.github.v3+json",
}

# labels.json 파일을 읽어서 레이블 생성
with open(".github/labels.json", "r", encoding="utf-8") as file:
    labels = json.load(file)

for label in labels:
    response = requests.post(url, headers=headers, json=label)
    if response.status_code == 201:
        print(f"Label '{label['name']}' created successfully.")
    elif response.status_code == 422:
        print(f"Label '{label['name']}' already exists.")
    else:
        print(f"Failed to create label '{label['name']}': {response.content}")
