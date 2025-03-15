FROM python:3.12-alpine

RUN adduser -D asottile
RUN addgroup allusers && addgroup asottile allusers

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt --force

WORKDIR /app

# Copy backend files
COPY app.py /app

EXPOSE 8080

USER asottile

CMD ["python", "app.py"]



