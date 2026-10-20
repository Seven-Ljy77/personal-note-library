FROM python:3.13-slim

WORKDIR /services

COPY requirements.txt .

# --no-cache-dir 不保留下载缓存
RUN pip install --no-cache-dir -r requirements.txt

# 第一个 app 是 wsl 内 app/ 目录，第二个 app 是复制到 WORKDIR/app/ 路径
COPY app/ ./app/

COPY alembic.ini .
COPY alembic/ ./alembic/
COPY tests/ ./tests/

# 规定默认启动命令，即 docker run 时运行的第一条命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
