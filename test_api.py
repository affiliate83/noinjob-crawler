import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('DATA_GO_KR_API_KEY')

print("=== 노인인력개발원 구인정보 API 테스트 ===")
url = "https://apis.data.go.kr/B552474/SenuriService/getJobList"
params = {
    'serviceKey': API_KEY,
    'numOfRows': 3,
    'pageNo': 1,
}
res = requests.get(url, params=params, timeout=15)
print(f"상태코드: {res.status_code}")
print(f"응답 앞 500자:\n{res.text[:500]}")

print("\n=== 복지서비스 API 테스트 ===")
url2 = "https://apis.data.go.kr/B554287/NationalWelfareInformationsV001/NationalWelfarelistV001"
params2 = {
    'serviceKey': API_KEY,
    'srchKeyCode': '001',
    'callTp': 'L',
    'numOfRows': 3,
    'pageNo': 1,
}
res2 = requests.get(url2, params=params2, timeout=15)
print(f"상태코드: {res2.status_code}")
print(f"응답 앞 500자:\n{res2.text[:500]}")
