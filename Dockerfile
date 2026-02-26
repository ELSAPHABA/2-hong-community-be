# 1. AWS Lambda Python 베이스 이미지 사용
FROM public.ecr.aws/lambda/python:3.9

# 2. Lambda 환경의 표준 작업 디렉토리 설정
WORKDIR ${LAMBDA_TASK_ROOT}

# 3. 빌드 도구 및 Poetry 설치
RUN pip install --no-cache-dir poetry

# 4. 의존성 파일 복사 (poetry.lock이 없는 경우를 대비해 pyproject.toml만 복사)
COPY pyproject.toml ./

# 5. 의존성 설치
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# 6. 전체 소스 코드 복사
COPY . .

# 7. Lambda 핸들러 설정 (파일명.변수명)
CMD ["main.handler"]
