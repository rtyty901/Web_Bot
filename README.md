# Web Scraping RAG 챗봇

웹 페이지 URL을 입력하여 스크래핑한 후, LangChain과 OpenAI를 사용하여 질문에 답변하는 RAG(Retrieval-Augmented Generation) 기반 챗봇입니다.

## 주요 기능

- 🌐 웹 페이지 스크래핑 및 자동 처리
- 🔍 벡터 기반 문서 검색 (FAISS)
- 💬 대화형 질의응답 인터페이스 (Gradio)
- ⚡ 벡터 저장소 캐싱으로 성능 최적화
- 🎛️ 청크 크기, 오버랩, Temperature 등 설정 가능

## 요구사항

- Python 3.12 이상
- Poetry (의존성 관리)
- OpenAI API 키 (GPT-4o-mini 및 임베딩 사용)

## 설치 방법

1. 저장소 클론:
```bash
git clone <repository-url>
cd Web_Scraping_RAG
```

2. 의존성 설치:
```bash
poetry install
```

3. 환경 변수 설정:
`.env` 파일을 생성하고 OpenAI API 키를 추가합니다:
```
OPENAI_API_KEY=your-api-key-here
```

## 사용 방법

1. 애플리케이션 실행:
```bash
poetry run python main.py
```

2. 웹 브라우저에서 Gradio 인터페이스 접속

3. 웹 페이지 URL 입력 및 설정 조정:
   - **웹 페이지 URL**: 분석할 웹 페이지 URL 입력 (예: https://example.com)
   - **Chunk Size**: 텍스트 분할 시 청크 크기 (기본값: 1000)
   - **Chunk Overlap**: 청크 간 오버랩 크기 (기본값: 200)
   - **Temperature**: 모델 생성 온도 (0.0~2.0)

4. 질문 입력 및 답변 받기

## 기술 스택

- **LangChain**: RAG 파이프라인 구현
  - `langchain-openai`: OpenAI 모델 및 임베딩
  - `langchain-community`: WebBaseLoader, FAISS 벡터 DB
  - `langchain-core`: RAG 체인 (LCEL)
- **OpenAI**: 
  - GPT-4o-mini: 답변 생성
  - text-embedding-3-small: 텍스트 임베딩
- **Gradio**: 웹 UI 인터페이스
- **FAISS**: 벡터 데이터베이스
- **BeautifulSoup4**: 웹 페이지 파싱
- **Requests**: HTTP 요청

## 지원 웹 페이지 형식

- **모든 HTTP/HTTPS 웹 페이지**
- URL은 `http://` 또는 `https://` 없이 입력해도 자동으로 추가됩니다
- 예: `example.com` → `https://example.com`

## 프로젝트 구조

```
Web_Scraping_RAG/
├── main.py              # 메인 애플리케이션
├── pyproject.toml       # Poetry 설정 및 의존성
├── poetry.lock          # 의존성 잠금 파일
├── README.md            # 프로젝트 문서
└── src/                 # 패키지 구조
```

## 주요 기능 설명

### 1. 웹 페이지 스크래핑
- LangChain의 WebBaseLoader를 사용하여 웹 페이지 내용 자동 추출
- HTML 파싱 및 텍스트 정제
- 다양한 웹 페이지 구조 지원

### 2. RAG 기반 질의응답
- 스크래핑된 텍스트를 벡터화하여 FAISS 벡터 저장소에 저장
- 사용자 질문과 관련된 텍스트 청크 검색
- 검색된 컨텍스트를 기반으로 GPT-4o-mini가 답변 생성

### 3. 벡터 저장소 캐싱
- 동일한 URL과 설정으로 생성된 벡터 저장소는 캐시하여 재사용
- 대화 세션 내 반복 질문 시 성능 향상

### 4. 웹 기반 사용자 인터페이스
- Gradio를 활용한 직관적인 웹 인터페이스
- URL 입력 및 실시간 질의응답

### 5. 고급 설정 옵션
- Chunk Size: 텍스트 분할 크기 조정
- Chunk Overlap: 청크 간 겹침 크기
- Temperature: 생성 다양성 조절

## 주의사항

- OpenAI API 사용에 따라 비용이 발생할 수 있습니다 (GPT-4o-mini: 토큰당 비용).
- 일부 웹 페이지는 로그인이 필요하거나 JavaScript로 동적 콘텐츠를 로드할 수 있어 스크래핑이 제한될 수 있습니다.
- 벡터 저장소는 메모리에 캐시되므로, 서버 재시작 시 다시 생성됩니다.
- 웹 페이지의 robots.txt 정책을 준수해야 합니다.

## 사용 시나리오

- 📰 뉴스/블로그 기사 분석
- 📚 문서/위키 페이지 질의응답
- 💼 기업 웹사이트 정보 조회
- 📖 온라인 문서/가이드 분석
- 🔍 웹 콘텐츠 요약 및 분석

## 라이선스

이 프로젝트는 개인 프로젝트입니다.

