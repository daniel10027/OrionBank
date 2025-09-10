FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
COPY migrations ./migrations
COPY .env.example ./.env
ENV PYTHONUNBUFFERED=1
EXPOSE 7000
CMD ["gunicorn", "app.wsgi:app", "-b", "0.0.0.0:7000", "-w", "2"]