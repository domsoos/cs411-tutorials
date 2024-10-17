FROM python:3.9-slim

WORKDIR /app

COPY . /app

# Disable pip's progress bar
ENV PIP_PROGRESS_BAR=off

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]

