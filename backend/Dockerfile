FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN addgroup --system app && adduser --system --ingroup app app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=app:app app.py entrypoint.sh ./
RUN chmod +x /app/entrypoint.sh

USER app

EXPOSE 8888

ENTRYPOINT ["/app/entrypoint.sh"]
