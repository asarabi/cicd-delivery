# 개발 규칙 및 컨벤션

## 프로젝트 구조

```
cicd-delivery/
├── src/              # 소스 코드
├── tests/            # 테스트 코드
├── pytest.ini        # pytest 설정
├── conftest.py       # pytest 공통 설정 및 fixtures
├── pyproject.toml    # 프로젝트 설정 및 의존성
├── requirements.txt  # Python 패키지 의존성
└── README.md         # 프로젝트 설명
```

## 코딩 규칙

### 1. 코드 스타일
- **포맷터**: Black 사용 (line-length: 100)
- **정렬**: isort 사용 (Black 프로필)
- **타입 힌팅**: 가능한 경우 타입 힌팅 사용
- **린터**: flake8, mypy 사용

### 2. 네이밍 컨벤션
- **모듈/파일**: `snake_case` (예: `user_service.py`)
- **클래스**: `PascalCase` (예: `UserService`)
- **함수/변수**: `snake_case` (예: `get_user_data`)
- **상수**: `UPPER_SNAKE_CASE` (예: `MAX_RETRY_COUNT`)
- **프라이빗**: `_leading_underscore` (예: `_internal_method`)

### 3. 테스트 규칙
- **테스트 파일**: `test_*.py` 형식
- **테스트 함수**: `test_*` 형식
- **테스트 클래스**: `Test*` 형식
- **테스트 위치**: `tests/` 디렉토리
- **마커 사용**: `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.slow`

### 4. 문서화
- **모듈 docstring**: 모든 모듈에 설명 추가
- **클래스 docstring**: 모든 클래스에 설명 추가
- **함수 docstring**: 공개 함수는 docstring 필수
- **인라인 주석**: 복잡한 로직에만 사용

### 5. Git 커밋 규칙
- **커밋 메시지**: 명확하고 간결하게 작성
- **형식**: `type: description` (예: `feat: 사용자 인증 기능 추가`)
- **타입**: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`

## 개발 워크플로우

### 1. 환경 설정
```bash
# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate  # Windows

# 의존성 설치
pip install -r requirements.txt
# 또는 개발 의존성 포함
pip install -e ".[dev]"
```

### 2. 코드 작성
1. `src/` 디렉토리에 소스 코드 작성
2. `tests/` 디렉토리에 테스트 코드 작성
3. 코드 포맷팅 및 린팅 확인

### 3. 테스트 실행
```bash
# 모든 테스트 실행
pytest

# 특정 테스트 파일 실행
pytest tests/test_example.py

# 커버리지 포함 실행
pytest --cov=src

# 특정 마커만 실행
pytest -m unit
pytest -m "not slow"
```

### 4. 코드 품질 검사
```bash
# 코드 포맷팅
black src/ tests/

# import 정렬
isort src/ tests/

# 린팅
flake8 src/ tests/

# 타입 체크
mypy src/
```

## Cursor + Claude 사용 가이드

### 1. Cursor 사용 시
- AI 어시스턴트를 활용한 코드 생성 및 리팩토링
- 자동 완성 및 제안 기능 활용
- 실시간 코드 리뷰

### 2. Claude 사용 시
- 복잡한 로직 설계 및 검토
- 아키텍처 결정 지원
- 문서화 및 주석 작성

### 3. 협업 규칙
- **일관성 유지**: 두 도구를 사용하더라도 동일한 코딩 스타일 유지
- **코드 리뷰**: 생성된 코드는 항상 검토 후 커밋
- **테스트 우선**: 기능 추가 시 테스트 코드 함께 작성

## 추가 규칙

### 1. 의존성 관리
- 프로덕션 의존성은 `pyproject.toml`의 `dependencies`에 추가
- 개발 의존성은 `[project.optional-dependencies]`의 `dev`에 추가
- `requirements.txt`는 간단한 설치를 위해 유지

### 2. 버전 관리
- Python 버전: 3.8 이상
- 주요 라이브러리 버전은 `pyproject.toml`에 명시

### 3. 에러 처리
- 명확한 에러 메시지 제공
- 적절한 예외 타입 사용
- 로깅 활용 (필요 시)

### 4. 성능
- 불필요한 중복 계산 방지
- 적절한 데이터 구조 선택
- 성능이 중요한 부분은 프로파일링

## 참고 자료
- [PEP 8](https://pep8.org/) - Python 스타일 가이드
- [pytest 문서](https://docs.pytest.org/)
- [Black 문서](https://black.readthedocs.io/)
