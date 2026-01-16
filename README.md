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

## Gerrit Manifest Delivery

이 프로젝트는 repo manifest를 파싱하여 hash revision이 아닌 프로젝트만 필터링하고, Gerrit으로 전송하는 도구입니다.

### 주요 기능

- Manifest 다운로드 및 파싱 (repo init 사용)
- Hash revision 필터링 (branch/tag만 전송)
- 브랜치 이름 변환 (날짜 suffix 추가 옵션)
- 레포지토리 이름 변환 (alias 추가 옵션)
- Gerrit으로 코드 전송 (SSH/HTTP 인증 지원)

### 사용법

1. 설정 파일 생성 (`config/config.yaml`):
   ```bash
   cp config/config.yaml.example config/config.yaml
   # 설정 파일 편집
   ```

2. 도구 실행:
   ```bash
   python -m src.cli.main -c config/config.yaml
   # 또는 설치 후
   cicd-delivery -c config/config.yaml
   ```

3. Dry-run 모드:
   ```bash
   cicd-delivery -c config/config.yaml --dry-run
   ```

### 설정 파일 예제

`config/config.yaml.example` 파일을 참고하세요.