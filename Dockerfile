FROM python:3.10.15-slim-bullseye

WORKDIR /app/src/backend

ENV VIRTUAL_ENV=/usr/local

COPY requirements.txt ./

RUN pip install --upgrade pip=="24.3.1" \
&& pip install uv=="0.5.14" \
&& uv pip install --python /usr/local --no-cache -r requirements.txt

COPY src/backend/ ./src/backend/

EXPOSE 3000

# CMD [ "fastapi", "dev", "backend/app/main.py", "--host", "0.0.0.0", "--port", "3000" ]