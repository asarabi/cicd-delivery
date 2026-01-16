# CI/CD Delivery Project

Python 기반 CI/CD 프로젝트입니다.

## 프로젝트 구조

```
cicd-delivery/
├── src/              # 소스 코드
├── tests/            # 테스트 코드
├── pytest.ini        # pytest 설정
├── conftest.py       # pytest 공통 설정
├── pyproject.toml    # 프로젝트 설정
├── requirements.txt  # 의존성 목록
└── CONTRIBUTING.md   # 개발 규칙 및 컨벤션
```

## 시작하기

### 환경 설정

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

### 테스트 실행

```bash
# 모든 테스트 실행
pytest

# 커버리지 포함 실행
pytest --cov=src

# 특정 테스트만 실행
pytest tests/test_example.py
```

### 코드 품질 검사

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

## 개발 규칙

자세한 개발 규칙 및 컨벤션은 [CONTRIBUTING.md](CONTRIBUTING.md)를 참고하세요.

## 기술 스택

- **언어**: Python 3.8+
- **테스트**: pytest
- **코드 품질**: black, flake8, mypy, isort