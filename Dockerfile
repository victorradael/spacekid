FROM python:3.14-slim

WORKDIR /build
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir . && rm -rf /build

RUN useradd --create-home --uid 1000 spacekid
USER spacekid

WORKDIR /project
ENTRYPOINT ["spacekid"]
