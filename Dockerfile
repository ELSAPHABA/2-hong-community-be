# Python slim 이미지를 사용하여 메모리 절약
FROM --platform=linux/amd64 python:3.9-slim

WORKDIR /app

# 빌드 시에만 필요한 도구 설치 및 캐시 삭제
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Poetry 설치 (전역 설치 대신 필요한 경우 가상환경 비활성화)
RUN pip install --no-cache-dir poetry

# 의존성 설치 (poetry.lock이 없으면 생성하며 설치됨)
COPY pyproject.toml /app/
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# 소스 코드 복사
COPY . /app/

# uvicorn 실행 (포트 8000 노출은 내부 통신용으로 사용됨)
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
