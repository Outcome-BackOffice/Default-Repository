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


# 기존 레이블 모두 삭제
def delete_existing_labels():
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        labels = response.json()
        for label in labels:
            delete_url = f"{url}/{label['name']}"
            delete_response = requests.delete(delete_url, headers=headers)
            if delete_response.status_code == 204:
                print(f"Label '{label['name']}' deleted successfully.")
            else:
                print(
                    f"Failed to delete label '{label['name']}': {delete_response.content}"
                )
    else:
        print(f"Failed to fetch labels: {response.content}")


# labels.json 파일을 읽어서 새로운 레이블 생성
def create_labels():
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


# 기존 레이블 삭제 및 새 레이블 생성 실행
delete_existing_labels()
create_labels()
