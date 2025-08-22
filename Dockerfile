FROM python:3.13-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN groupadd --gid 1000 app \
    && useradd --uid 1000 --gid app --shell /bin/bash --create-home app

    RUN apt-get update && apt-get install -y --no-install-recommends \
      curl ca-certificates gnupg apt-transport-https \
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg \
       | gpg --dearmor -o /etc/apt/keyrings/google-cloud.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/google-cloud.gpg] https://packages.cloud.google.com/apt cloud-sdk main" \
       > /etc/apt/sources.list.d/google-cloud-sdk.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
         google-cloud-cli \
         google-cloud-cli-gke-gcloud-auth-plugin \
         kubectl \
    && rm -rf /var/lib/apt/lists/*

    USER app
ENV PATH="/home/app/.local/bin:${PATH}"

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

RUN pip install --user --no-cache-dir awscli

WORKDIR /home/app
COPY --chown=app:app uv.lock* pyproject.toml ./

RUN --mount=type=cache,target=/home/app/.cache/uv,uid=1000,gid=1000 \
    uv sync --frozen --no-dev

COPY --chown=app:app . .
CMD ["uv", "run", "python", "-m", "app"]
