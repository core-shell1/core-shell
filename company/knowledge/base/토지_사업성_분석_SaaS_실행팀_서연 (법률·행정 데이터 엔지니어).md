
### 국토교통부 토지이용규제 공공데이터 API 활용 방법 및 제공 항목 2024
### 1. 주요 API 목록 (2024-2025 최신)
국토교통부 토지이용규제 공공데이터는 **공공데이터포털(data.go.kr)**과 **토지이음(eum.go.kr)**에서 주로 제공. 핵심 2개 API 활용[1][2].

| API명 | 제공기관 | 데이터포맷 | 트래픽(일) | 키워드 | 수정일 |
|-------|----------|------------|-------------|--------|--------|
| **지역지구별 토지이용규제정보** | 국토교통부 | JSON/XML (RestAPI) | 개발:1,000 / 운영:신청증가 | 지역지구코드, 법령정보, 제한규정 | 2025-07-01[1] |
| **토지이용규제법령정보서비스** | 국토교통부 | XML (RestAPI) | 개발:1,000 / 운영:신청증가 | 토지이용행위, 규제안내서, 조례정보 | 2025-07-01[2] |

**보조: 토지이음 파일데이터** (API 아닌 ZIP 다운로드, 월 업데이트)
- 행위제한정보: 전국 38MB (2024-11-01)[5]
- 법령정보: 전국 9MB (2024-12-01)[8]

### 2. 제공 항목 (핵심 필드 예시)
- **지역지구별 토지이용규제정보**: 관할지역코드, 지역지구코드, 법령정보, 조항, 제한규정 (건축/용도 제한 등)[1].
- **토지이용규제법령정보**: 토지이용행위 규제, 법령/조례 내용, 규제내용[2].
- **토지이음 행위제한**: eclgyArRate(생태면적률 23.1%), devlopRttdrRelisAr(개발제한 해제면적 4500㎡), lnParkAr(공원면적 3202㎡)[4].

### 3. 활용 방법 (실전 5단계, 2024 기준)
1. **회원가입/인증키 발급**: data.go.kr 회원가입 → 마이페이지 → 인증키 신청 (무료, 즉시)[1][2][3].
2. **활용신청**: API 상세페이지 → **Ctrl+클릭 활용신청** → 새창 신청 → 마이페이지 '개발계정 상세보기'에서 **ServiceKey 복사** (자동승인)[3].
3. **API 호출 URL 구성**:
   ```
   GET https://apis.data.go.kr/{서비스ID}/{서비스명}?ServiceKey={인증키}&{쿼리파라미터}
   ```
   - 예: 토지이용규제법령 (ID 확인 후)[2].
4. **샘플코드 (JavaScript, 즉시 테스트)**[4]:
   ```javascript
   var xhr = new XMLHttpRequest();
   var url = 'http://apis.data.go.kr/B090026/LandUseService/getInfo';  // URL 예시
   var queryParams = '?' + encodeURIComponent('ServiceKey') + '={YOUR_KEY}';
   queryParams += '&' + encodeURIComponent('mgtNo') + '=' + encodeURIComponent('ND2009A007');  // 필수: 사업코드
   queryParams += '&' + encodeURIComponent('type') + '=' + encodeURIComponent('json');
   xhr.open('GET', url + queryParams);
   xhr.onreadystatechange = function() {
       if (this.readyState == 4) console.log(this.responseText);  // JSON 응답
   };
   xhr.send('');
   ```
   - **Python 예시** (requests 라이브러리):
     ```python
     import requests
     url = "http://apis.data.go.kr/B090026/LandUseService/getInfo"
     params = {'ServiceKey': 'YOUR_KEY', 'mgtNo': 'ND2009A007', 'type': 'json'}
     response = requests.get(url, params=params).json()
     print(response)  # {'mgtno': 'ND2009A007', 'eclgyArRate': 23.1, ...}
     ```
5. **트래픽 관리/운영 전환**: 1,000회 초과 시 마이페이지 '운영계정 신청' + 활용사례 등록 → 증가[2]. 오류: 공공데이터지원센터 문의[1].

### 4. 실전 팁 (

### 국가법령정보센터 OpenAPI 법령 조문 자동 수집 및 버전 관리 방법
### 1. API 인증 및 초기 설정 (실전 5분 셋업)
- **회원가입 & 키 발급**: [open.law.go.kr](https://open.law.go.kr) → 공동활용센터 → Open API 신청 → 승인(1-2일). 발급 **OC 키** 저장 (e.g., `OC=your_key`).[1][7][8]
- **호출 형식**: `http://www.law.go.kr/DRF/{service}.do?OC={your_key}&target=law&type=XML&...` (XML 추천: 조문 구조 파싱 용이).[3]
- **제한**: 일일 10,000건, 초과 시 블록. 배치 스케줄링 필수 (e.g., cron 00:00).[8]

### 2. 조문 자동 수집 프레임워크 (Python 코드 + 단계)
**핵심 API 체인**:
1. **목록 조회** → 현행법령(시행일) 목록: `lawSearch.do?OC={key}&target=law&type=XML&sort=시행일자` → **법령ID** 추출.[1][3]
2. **본문 수집** → 현행법령 본문: `lsEfYdInfo.do?OC={key}&lawId={ID}&type=XML` → 조문/XML 풀텍스트.[1][9]
3. **상세 조항** → 조항호목: `lsNwJoList.do?OC={key}&lawId={ID}&type=XML`.[1][10]

**Python 실전 코드** (requests + xml.etree + pandas, 100법령/분 처리):
```python
import requests
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime
import hashlib  # 버전 해시

def fetch_law_list(oc_key, page=1, rows=100):
    url = f"http://www.law.go.kr/DRF/lawSearch.do?OC={oc_key}&target=law&type=XML&sort=시행일자&resultCnt={rows}&page={page}"
    resp = requests.get(url)
    root = ET.fromstring(resp.text)
    laws = []
    for law in root.findall('.//법령'):
        laws.append({
            '법령ID': law.find('법령ID').text,
            '법령명': law.find('법령명한글').text,
            '시행일자': law.find('시행일자').text
        })
    return pd.DataFrame(laws)

def fetch_full_text(oc_key, law_id):
    url = f"http://www.law.go.kr/DRF/lsEfYdInfo.do?OC={oc_key}&lawId={law_id}&type=XML"
    resp = requests.get(url)
    root = ET.fromstring(resp.text)
    
    # 조문 파싱 (핵심: 조문 > 조문단위 > 조문내용/항/호)
    articles = []
    for 조문 in root.findall('.//조문'):
        art = {
            '조문번호': 조문.find('조문번호').text,
            '조문내용': 조문.find('조문내용').text,
            '항': [h.find('항내용').text for h in 조문.findall('.//항')],
            '호': [h.find('호내용').text for h in 조문.findall('.//호')]
        }
        articles.append(art)
    
    # 버전 해시: 내용 MD5 (변경検知)
    content_hash = hashlib.md5(str(articles).encode()).hexdigest()
    return {'law_id': law_id, 'articles': articles, 'version_hash': content_hash, 'fetch_date': datetime.now().isoformat()}

# 배치 실행 예: 상위 10법령 수집
oc_key = 'YOUR_OC_KEY'
laws_df = fetch_law_list(oc_key, rows=10)
all_data = []
for law_id in laws_df['법령ID']:
    data = fetch_full_text(oc_key, law_id)
    all_data.append(data)
pd.DataFrame(all_data).to_json('laws_v1.json', orient='records')  # JSON 저장
```
- **성능**: 1법령 0.5초, 2,000법령/시간. Error handling: `try-except + retry(3)` 추가.[2]

**XML 구조 핵심 (파싱 타겟)**[2]:
```
<법령-법령키>
  <기본정보><법령I

### 부동산 개발 인허가 행정심판·판례 데이터 수집 출처 및 크롤링 합법 범위
### **주요 데이터 출처 (오픈API/공공DB 우선)**
- **법제처 중앙행정심판위원회 API**: 행정심판 사례 목록(사건번호, 재결일자, 사건명, 처분청, 재결결과, 결정요지) 무료 XML 제공. 부동산 인허가(건축/개발허가 취소 등) 필터링 가능. 이용허락 **제한 없음**[1].
- **법제처 국가법령정보센터**: 행정심판 재결례, 유권해석, 판례 통합 검색. 부동산개발업 관리법 제4조/제11조 관련 사례 다수[9][8].
- **대법원/행정법원 판례 DB**: glaw.scourt.go.kr에서 "부동산 개발 인허가 행정심판" 키워드 검색. 서울행법 99구23709(청문 미실시 취소), 서울행심 97-207(영업정지 취소) 등 실전 판례[4].
- **지역 행정심판위원회**: 서울시/지자체 사이트(예: klri.re.kr) 건축법 위반 시정명령 사례[2]. 동구청 행정절차 안내(처분기준 공표, 청문 필수)[4].

| 출처 | 키 필드 | 부동산 인허가 사례 예시 | 접근성 |
|------|---------|-------------------------|--------|
| 법제처 API[1] | 사건번호, 결정요지 | 개발허가 취소 심판 | 무료 XML API |
| 법제처 moleg[9] | 재결례/유권해석 | 부동산개발업 등록 제한 | 웹 검색 |
| 대법원 판례[4] | 판결문 | 인허가 철회 청문 위반 | 무료 검색 |

### **크롤링 합법 범위 (저작권법·정보통신망법 준수)**
- **합법**: 공공데이터포털(data.go.kr) CC0/CC-BY 라이선스 데이터 무제한 수집/재가공. 법제처 API **로그인 후 호출 무한**[1]. robots.txt 확인 후 rate limit(초당 1회) 준수[1].
- **제한**: 민간 사이트(klri.re.kr 등) robots.txt 금지 시 불가. 개인정보(주민번호) 마스킹 필수. 상업적 2차 가공 시 출처 명시(CC-BY)[1][9].
- **위반 사례 피하기**: API 초과(488 이용신청 기록 있음) 시 블록. 판례 전체 복제 금지, 요약만(저작권법 제28조 공표작 활용 한도 1/3)[4].
- **프레임워크**:
  1. 출처 robots.txt 확인.
  2. API 우선(법제처: http://open.law.go.kr/LSO/openApi/deccList).
  3. Python Selenium/BeautifulSoup: 헤더 User-Agent 명시, 지연 5초.
  4. 저장: CSV(사건번호|키워드|결과|날짜).

### **실전 적용 팁 (부동산 개발 리스크 예측)**
- **쿼리 예시**: API params `searchType=KS&searchWord=부동산+개발+인허가` → 2025.07 수정 데이터 1000+건 추출[1].
- **통계 활용**: 재결결과 비율(취소 20%, 유지 70%)으로 인허가 승률 85% 예측[4].
- **위험 지표**: 청문 미실시(취소율 90%), 처분기준 미공표(무효)[4]. 개발행위허가 협의(경관/환경) 사례 50% 불허[3].
- **자동화 스크립트 틀**:
```python
import requests
url = "http://open.law.go.kr/LSO/openApi/deccList"
params = {'searchWord': '부동산 개발 인허가', 'pageNo': 1}
response = requests.get(url, params=params)
# XML 파싱 → CSV 저장
```
- **업데이트 주기**: 법제처 수정일 2025-07-08 기준 매월 크롤[1]. 이해충돌법(부동산 미공개정보 금지) 준수[5][6

### RAG용 법률 문서 청킹 전략 — 조문 단위 vs 항 단위 임베딩 품질 비교
### 법률 문서 RAG 청킹: **조문 단위 vs 항 단위** 임베딩 품질 비교

**항(하위 조항) 단위 청킹이 조문 단위보다 검색 정밀도 10-15% 우수 (Recall@5 기준)**. 법률 문서의 계층 구조(조 > 항 > 단서)에서 항 단위가 문맥 보존과 세밀 검색에 최적화되며, 조문 단위는 과도한 노이즈로 임베딩 품질 저하[1][3][4].

#### 실증 데이터 비교 (벤치마크 기준)
| 청킹 단위 | Recall@5 | Cosine 유사도 | 청크 크기 (토큰) | 메모리 비용 | 추천 법령 유형[2][3][4] |
|-----------|----------|---------------|------------------|-------------|-------------------------|
| **조문 단위** | 72-78% | 0.82 | 600-1000 | 기준 | 단순 조문 (행정법) |
| **항 단위** | 85-92% | 0.91 | 300-600 | 1.5배 | 복합 조문 (민법, 형법: 단서/준용 참조) |

- **조문 단위 단점**: 조문 길이 불균형 (짧으면 문맥 단절 20%↑, 길면 정밀도 ↓15%)[3]. 참조 조문(예: "제X조 준용") 무시 시 검색 완결성 25% 하락[3].
- **항 단위 우위**: 논리 경계(항목 번호) 활용, 의미 유사도 60% 임계로 동적 분할 → **87% 정확도** (MDPI 2025)[1][2]. E5 임베딩 모델에서 고정 청킹比 12%p ↑[2].

#### 구현 프레임워크 (Python, ChromaDB 적용)
```python
import re
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from openai import OpenAI

client = OpenAI()
chroma_client = chromadb.PersistentClient(path="./legal_db")

def legal_chunk(text: str, unit: str = "항") -> list[dict]:
    """법률 문서 청킹: 조/항 추출 + 메타데이터"""
    chunks = []
    if unit == "조문":
        pattern = r'제(\d+)조\s*(.*?)(?=제\d+조|$)'
    else:  # 항 단위
        pattern = r'제(\d+)조\s*(\d+항.*?)(?=\d+항|제\d+조|$)'
    
    for match in re.finditer(pattern, text, re.DOTALL):
        chunk_id, 조문, content = f"legal_{match.group(1)}", match.group(1), match.group(2).strip()
        embedding = client.embeddings.create(input=[content], model="text-embedding-3-large", dimensions=1024).data[0].embedding
        chunks.append({"id": chunk_id, "text": content, "metadata": {"unit": unit, "조문": 조문}, "embedding": embedding})
    return chunks

# 벡터 저장 & 검색
ef = OpenAIEmbeddingFunction(model_name="text-embedding-3-large")
collection = chroma_client.get_or_create_collection("legal_rag", embedding_function=ef, metadata={"hnsw:M": 32, "hnsw:ef_construction": 200})

chunks = legal_chunk("제1조 1항 ... 제2조 1항 ...", unit="항")  # 항 단위 예시
collection.add(documents=[c["text"] for c in chunks], metadatas=[c["metadata"] for c in chunks], ids=[c["id"] for c in chunks])

# 검색 (K=6-8 추천[4])
results = collection.query(query_texts=["계약 해지 조건"], n_results=8, where={"unit": "항"})
# 출력: 거리<0.2 항목 우선 (임베딩 품질 ↑)
```

#### 최적화 팁 (성능 20%↑ 사례)
- **하이브리드**: 조문+참조 항 묶기 (완결성 25%↑)[3]. 메타데이터 필터 (`where={"조문": "제101조"}`)[5].
- **임베딩 모델**: text-embedding-3-large (dimensions=1024, 비용 50%↓)

### 도시개발법·택지개발촉진법·농지법 특례 조항 자동 분류 체계 설계 방법
### **특례 조항 자동 분류 체계 설계 프레임워크**
**핵심 목표**: 도시개발법(제71조의2 결합개발 특례[1][2]), 택지개발촉진법(건폐율·용적률 완화[7]), 농지법(농지전용 특례) 조항을 NLP+규칙 기반으로 95% 정확도 자동 분류. 실전 적용: 법령 텍스트 입력 → 특례 유형/적용조건/제한 자동 태깅 → 개발사업 타당성 검토 1시간 단축.

#### **1. 데이터 수집 & 라벨링 (준비 단계, 20% 노력)**
- **소스**: 국가법령정보센터[2][3] 풀텍스트(도시개발법 시행령 제85조의4 특례[1]), 지침서[4], 유권해석[9]. 1,000+ 조항 대상.
- **라벨링 사례** (3개 법률 특례 유형):
  | 법률 | 특례 조항 예시 | 유형 | 조건 | 제한 |
  |------|---------------|------|------|------|
  | 도시개발법 | 제85조의4 결합개발 기준 완화[1] | 개발계획 완화 | 사업시행지구 1만㎡↑ 분할[2] | 자연재해지역 우선개발[2] |
  | 택지개발촉진법 | 건폐율·용적률 특례[7] | 건축 규제 완화 | 리츠·신탁 시행 | 성장거점형 사업 |
  | 농지법 | 농지전용 허용 | 토지용도 변경 | 도시개발구역 지정 시 | 생산녹지 30%↓ 한정[2] |
- **도구**: LabelStudio (무료). 100개 샘플 수작업 → Active Learning으로 80% 자동.

#### **2. 분류 모델 아키텍처 (코어 엔진, 50% 노력)**
**하이브리드 접근**: BERT(KorBERT) + 규칙 매칭 → F1-score 0.93 목표 (테스트: 500조항).
```
입력: "제85조의4(특례 적용). ① 지정권자는 법 제71조의2에 따라 결합개발 등에 관한 적용 기준 완화"[1]
↓
1. 키워드 룰 필터 (정확도 85%, 속도 1ms/조항)
   - 특례 트리거: "특례", "완화", "제외", "허가 면제", "제한 적용하지 아니함"[2]
   - 법률별: "도시개발법 제71조의2", "농지법 전용", "택지개발 촉진"
   - 출력: {유형: "기준완화", 법률: "도시개발법"}

2. KorBERT fine-tuning (정확도 보강)
   ```python
   from transformers import BertTokenizer, BertForSequenceClassification
   tokenizer = BertTokenizer.from_pretrained('monologg/kobert')
   model = BertForSequenceClassification.from_pretrained('monologg/kobert', num_labels=12)  # 12=유형(완화/전용/면제 등) x 3법률
   # 학습 데이터: 특례 긍정(70%), 부정(30%)
   inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
   outputs = model(**inputs).logits  # 확률: [0.92 완화특례]
   ```
   - 하이퍼: LR 2e-5, Epoch 3, Batch 16. GPU 1대 2시간.

3. 후처리: 조건별 계층 분류
   - IF "1만㎡ 이상"[2] → {규모: "대형", 적용: "시·도지사 지정"}
   - 출력 JSON: {"조항": "제85조의4", "특례_유형": "결합개발 완화", "위험도": "저(우선개발 준수)"}
```

#### **3. 구현 & 배포 (운영화, 20% 노력)**
- **파이프라인**:
  1. PDF/텍스트 입력 → PyMuPDF 추출.
  2. LangChain으로 청크(500자) 분할 → 병렬 분류 (10조항/초).

