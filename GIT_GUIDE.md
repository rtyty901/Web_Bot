# Git 업로드 가이드

## VSCode에서 Git에 업로드하는 방법

### 방법 1: VSCode GUI 사용 (추천)

1. **소스 제어 패널 열기**
   - 왼쪽 사이드바에서 소스 제어 아이콘(분기 모양) 클릭
   - 또는 `Ctrl + Shift + G`

2. **변경사항 스테이징**
   - "변경사항" 섹션에서 커밋할 파일 선택
   - 파일 옆의 `+` 버튼 클릭하거나
   - 모든 파일을 추가하려면 "변경사항" 옆의 `+` 버튼 클릭

3. **커밋 메시지 작성**
   - 상단의 메시지 입력란에 커밋 메시지 입력
   - 예: "초기 프로젝트 설정: PDF RAG 챗봇 구현"

4. **커밋 실행**
   - `Ctrl + Enter` 또는 체크마크 버튼 클릭

5. **원격 저장소 연결 (GitHub 등)**
   - 소스 제어 패널에서 `...` 메뉴 클릭
   - "원격" > "원격 추가" 선택
   - 원격 이름: `origin`
   - 원격 URL: GitHub 저장소 URL 입력
     - 예: `https://github.com/사용자명/pdf-bot.git`

6. **푸시 (Push)**
   - `...` 메뉴에서 "푸시" 선택
   - 또는 하단 상태바의 업로드 화살표 클릭

### 방법 2: 터미널 사용

```bash
# 1. 모든 파일 추가
git add .

# 2. 커밋
git commit -m "초기 프로젝트 설정: PDF RAG 챗봇 구현"

# 3. 원격 저장소 추가 (GitHub 저장소 생성 후)
git remote add origin https://github.com/사용자명/pdf-bot.git

# 4. 푸시
git branch -M main  # master를 main으로 변경 (선택사항)
git push -u origin main
```

### GitHub 저장소 생성 방법

1. GitHub.com에 로그인
2. 우측 상단 `+` 버튼 > "New repository" 클릭
3. Repository name: `pdf-bot` (또는 원하는 이름)
4. Public/Private 선택
5. **"Initialize this repository with a README" 체크하지 않기** (이미 README.md가 있음)
6. "Create repository" 클릭
7. 생성된 저장소 URL을 복사하여 위의 원격 저장소 URL로 사용

### 주의사항

- `.env` 파일은 Git에 올라가지 않도록 `.gitignore`에 포함되어 있습니다
- API 키 등 민감한 정보는 절대 커밋하지 마세요
- `poetry.lock`은 커밋하는 것이 좋습니다 (의존성 버전 고정)
