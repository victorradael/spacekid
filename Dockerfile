FROM python:3.14-slim

RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY pyproject.toml README.md ./
COPY src ./src
ARG VERSION
RUN if [ -n "$VERSION" ]; then sed -i "s/^version = .*/version = \"$VERSION\"/" pyproject.toml; fi \
    && pip install --no-cache-dir . && rm -rf /build

RUN useradd --create-home --uid 1000 spacekid
USER spacekid

WORKDIR /project
ENTRYPOINT ["spacekid"]
