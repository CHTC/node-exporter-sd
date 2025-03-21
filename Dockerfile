FROM python:python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY run.py .

RUN pip install aiohttp

EXPOSE 8000

CMD ["python", "run.py"]
