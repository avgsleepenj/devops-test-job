FROM python:3.8-slim
#добавляем non-root пользователя 
RUN groupadd -r appuser && useradd -r -g appuser appuser 
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
USER appuser
COPY app.py .
ENV PORT=8888
CMD ["python", "app.py"]
