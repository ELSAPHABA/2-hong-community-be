# 1. 표준 Python 베이스 이미지 사용 (ECS, 로컬, Lambda 공용)
FROM python:3.9-slim

# 2. AWS Lambda Web Adapter 추가 (Lambda에서도 uvicorn을 그대로 사용 가능하게 함)
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.7.0 /lambda-adapter /opt/extensions/lambda-adapter

# 3. 작업 디렉토리 설정
WORKDIR /app

# 4. 필수 빌드 도구 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 5. Poetry 설치 및 의존성 복사
RUN pip install --no-cache-dir poetry
COPY pyproject.toml poetry.lock* ./

# 6. 의존성 설치
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# 7. 전체 소스 코드 복사
COPY . .

# 8. 포트 설정 (Web Adapter 기본값은 8080이지만, uvicorn 기본값인 8000으로 설정 가능)
ENV PORT=8000
EXPOSE 8000

# 9. 실행 명령어 (ECS/로컬/Lambda 공용)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
