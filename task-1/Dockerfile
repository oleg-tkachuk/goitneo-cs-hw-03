FROM python:3.12

WORKDIR /app

RUN adduser --disabled-password --no-create-home --gecos 'Non-privileged application user' appuser

RUN apt-get update && \
    apt-get install -y netcat-traditional && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install psycopg2-binary \
    && pip3 install faker

COPY scripts/seed.py /app/seed.py
COPY scripts/entrypoint.sh /entrypoint.sh

RUN chmod +x /app/seed.py /entrypoint.sh

USER appuser

ENTRYPOINT ["/app/entrypoint.sh"]