FROM python:3.11-slim

COPY requirements-test.txt /tmp/requirements-test.txt
RUN python -m pip install --no-cache-dir --disable-pip-version-check -r /tmp/requirements-test.txt \
    && rm /tmp/requirements-test.txt

WORKDIR /workspace
ENV PYTHONDONTWRITEBYTECODE=1
