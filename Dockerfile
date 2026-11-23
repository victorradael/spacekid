# Both stages use the same Alpine release (pinned by digest; Dependabot bumps it).
FROM alpine:3.24@sha256:f59abe656b692d901e184be3445e084786602108599d2a51d229c0f5a48c71bf AS build

RUN apk add --no-cache python3 py3-pip py3-setuptools

WORKDIR /build
COPY pyproject.toml README.md ./
COPY src ./src
ARG VERSION
RUN if [ -n "$VERSION" ]; then \
        echo "$VERSION" | grep -Eq '^[0-9]+\.[0-9]+\.[0-9]+([-+][0-9A-Za-z.-]+)?$' \
            || { echo "invalid VERSION: $VERSION" >&2; exit 1; }; \
        sed -i "s/^version = .*/version = \"$VERSION\"/" pyproject.toml; \
    fi \
    && pip install --no-cache-dir --break-system-packages --no-build-isolation --prefix=/out .

FROM alpine:3.24@sha256:f59abe656b692d901e184be3445e084786602108599d2a51d229c0f5a48c71bf

# Latest security fixes of the base; only python3 and git on top; the unused
# parts of the standard library are removed; no setuid/setgid programs remain.
RUN apk upgrade --no-cache \
    && apk add --no-cache python3 git \
    && adduser -D -u 1000 spacekid \
    && cd /usr/lib/python3* \
    && rm -rf ensurepip idlelib lib2to3 pydoc_data tkinter turtledemo test unittest \
        asyncio multiprocessing sqlite3 curses dbm distutils pydoc.py turtle.py \
        lib-dynload/_sqlite3* lib-dynload/_tkinter* lib-dynload/_curses* lib-dynload/_dbm* \
    && find /usr/lib/python3* -name __pycache__ -prune -exec rm -rf {} + \
    && find / -xdev -type f -perm /6000 -exec chmod a-s {} +

COPY --from=build /out/ /usr/

USER spacekid
WORKDIR /project
ENTRYPOINT ["spacekid"]
