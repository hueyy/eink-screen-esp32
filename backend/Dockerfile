FROM python:3.13.1-bookworm

ENV TZ="Asia/Singapore"

RUN curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg && \
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list && \
    apt-get update && apt-get install -y \
    debian-keyring \
    debian-archive-keyring \
    apt-transport-https \
    curl \
    gnupg \
    tini \
    pipx \
    caddy && \
    # install Fira Sans
    mkdir -p /usr/share/fonts/truetype/fira && \
    curl -L https://github.com/mozilla/Fira/archive/refs/tags/4.202.zip -o fira.zip && \
    unzip fira.zip && \
    mv Fira-4.202/ttf/FiraSans*.ttf /usr/share/fonts/truetype/fira/ && \
    rm -rf Fira-4.202 fira.zip && \
    fc-cache -f -v && \
    # install poetry
    pipx ensurepath && \
    pipx install poetry==1.8.4 && \
    # install nodejs
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get update && \
    apt-get install -y nodejs && \
    # install pnpm
    npm install -g pnpm && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /srv
COPY Caddyfile pnpm-lock.yaml poetry.lock pyproject.toml package.json pnpm-lock.yaml ./
RUN pnpm install && \
    $HOME/.local/bin/poetry add pytest-playwright && \
    $HOME/.local/bin/poetry install && \
    $HOME/.local/bin/poetry run playwright install --with-deps chromium
COPY server ./server

RUN pnpm dlx @tailwindcss/cli -i ./server/styles/main.css -o ./server/static/styles/main.css --minify && \
    cp -f node_modules/htmx.org/dist/htmx.min.js server/static/scripts/htmx.min.js

ENTRYPOINT ["/usr/bin/tini", "--"]

EXPOSE 8000

CMD ["sh", "-c", "caddy run & $HOME/.local/bin/poetry run gunicorn -w 2 -b localhost:5000 server.server:app --access-logfile -"]