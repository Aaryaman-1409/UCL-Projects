
FROM python:3-slim as base
WORKDIR /app
COPY . .
RUN python -m pip install pygame

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser
USER appuser

# What the container should run when it is started.
ENTRYPOINT [ "python", "cmdline.py" ]
