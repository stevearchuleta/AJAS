# syntax=docker/dockerfile:1.7

# ============================================================
# BUILD THE NEXT.JS STANDALONE APPLICATION.
# ============================================================
FROM node:24-bookworm-slim AS builder

# ============================================================
# SET THE MONOREPO BUILD DIRECTORY.
# ============================================================
WORKDIR /workspace

# ============================================================
# DISABLE NEXT.JS TELEMETRY DURING THE CLOUD BUILD.
# ============================================================
ENV CI=1 \
    NEXT_TELEMETRY_DISABLED=1

# ============================================================
# USE THE REPOSITORY-PINNED NPM VERSION.
# ============================================================
RUN npm install --global npm@10.9.2

# ============================================================
# COPY PACKAGE MANIFESTS FIRST FOR DEPENDENCY-LAYER CACHING.
# ============================================================
COPY package.json package-lock.json ./
COPY apps/web/package.json apps/web/package.json
COPY apps/worker/package.json apps/worker/package.json
COPY packages/core/package.json packages/core/package.json

# ============================================================
# INSTALL THE EXACT LOCKFILE DEPENDENCY GRAPH.
# ============================================================
RUN npm ci --no-audit --no-fund

# ============================================================
# COPY THE REMAINING RUNTIME-RELEVANT SOURCE TREE.
# ============================================================
COPY . .

# ============================================================
# BUILD ONLY THE AJAS WEB WORKSPACE.
# ============================================================
RUN npm run build --workspace @ajas/web

# ============================================================
# REQUIRE THE EXPECTED MONOREPO STANDALONE SERVER OUTPUT.
# ============================================================
RUN test -f apps/web/.next/standalone/apps/web/server.js

# ============================================================
# COPY STATIC ASSETS INTO THE STANDALONE SERVER TREE.
# ============================================================
RUN mkdir -p apps/web/.next/standalone/apps/web/.next/static \
    && cp -R apps/web/.next/static/. apps/web/.next/standalone/apps/web/.next/static/ \
    && if [ -d apps/web/public ]; then \
         mkdir -p apps/web/.next/standalone/apps/web/public; \
         cp -R apps/web/public/. apps/web/.next/standalone/apps/web/public/; \
       fi

# ============================================================
# CREATE THE MINIMAL NON-ROOT RUNTIME IMAGE.
# ============================================================
FROM node:24-bookworm-slim AS runtime

# ============================================================
# SET THE RUNTIME APPLICATION DIRECTORY.
# ============================================================
WORKDIR /app

# ============================================================
# CONFIGURE THE NEXT.JS STANDALONE SERVER FOR CONTAINER APPS.
# ============================================================
ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1 \
    HOSTNAME=0.0.0.0 \
    PORT=3000

# ============================================================
# COPY ONLY THE TRACED STANDALONE RUNTIME.
# ============================================================
COPY --from=builder --chown=node:node /workspace/apps/web/.next/standalone ./

# ============================================================
# DROP ROOT PRIVILEGES BEFORE STARTING THE WEB SERVER.
# ============================================================
USER node

# ============================================================
# DOCUMENT THE CONTAINER INGRESS PORT.
# ============================================================
EXPOSE 3000

# ============================================================
# START THE MONOREPO STANDALONE SERVER.
# ============================================================
CMD ["node", "apps/web/server.js"]
