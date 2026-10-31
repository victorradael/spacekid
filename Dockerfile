FROM alpine:3.22 AS build

RUN apk add --no-cache python3 py3-pip py3-setuptools

WORKDIR /build
COPY pyproject.toml README.md ./
COPY src ./src
ARG VERSION
RUN if [ -n "$VERSION" ]; then sed -i "s/^version = .*/version = \"$VERSION\"/" pyproject.toml; fi \
    && pip install --no-cache-dir --break-system-packages --no-build-isolation --prefix=/out .

FROM alpine:3.22

# Only python3 and git; the unused parts of the standard library are removed.
RUN apk add --no-cache python3 git \
    && adduser -D -u 1000 spacekid \
    && cd /usr/lib/python3* \
    && rm -rf ensurepip idlelib lib2to3 pydoc_data tkinter turtledemo test unittest \
        asyncio multiprocessing sqlite3 curses dbm distutils pydoc.py turtle.py \
        lib-dynload/_sqlite3* lib-dynload/_tkinter* lib-dynload/_curses* lib-dynload/_dbm* \
    && find /usr/lib/python3* -name __pycache__ -prune -exec rm -rf {} +

COPY --from=build /out/ /usr/

USER spacekid
WORKDIR /project
ENTRYPOINT ["spacekid"]
