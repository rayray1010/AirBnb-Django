# 使用官方的 Python 映像作為基礎映像
FROM --platform=linux/amd64 python:3.11.4-alpine3.18
# FROM python:3.11.4-alpine3.18


# 設置工作目錄
WORKDIR /app

# 安裝編譯工具和依賴
RUN apk add --no-cache gcc musl-dev libffi-dev
# 複製項目中的 requirements.txt 文件到容器中
COPY requirements.txt .

# 安裝項目的依賴
RUN pip install -r requirements.txt

# 複製整個項目到容器中的工作目錄
COPY . .

# 開放 Django 應用的預設端口（假設為 8000）
EXPOSE 8000


# 執行 Django 項目（這裡使用 gunicorn 作為伺服器，你可以根據需要選擇其他伺服器）
# CMD ["python", "manage.py", "migrate"]
CMD ["gunicorn", "backend.wsgi", "--bind", ":8000", "--access-logfile", "-", "--error-logfile", "-"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]