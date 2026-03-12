# 1. 표준 Python 베이스 이미지 사용
FROM python:3.9-slim

# 2. Python 환경 변수 설정 (K8s 로그 확인 및 성능 최적화)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

# 3. AWS Lambda Web Adapter 추가 (Lambda 호환성 유지)
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.7.0 /lambda-adapter /opt/extensions/lambda-adapter

# 4. 작업 디렉토리 설정
WORKDIR /app

# 5. 필수 빌드 도구 및 유저 생성
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && useradd -m -u 1000 appuser \
    && rm -rf /var/lib/apt/lists/*

# 6. Poetry 설치 및 의존성 복사
RUN pip install --no-cache-dir poetry
COPY pyproject.toml poetry.lock* ./

# 7. 의존성 설치
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# 8. 전체 소스 코드 복사 및 권한 설정
COPY . .
RUN chown -R appuser:appuser /app

# 9. 비루트(Non-root) 유저로 실행
USER appuser

# 10. 포트 설정
EXPOSE 8000

# 11. 실행 명령어
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

