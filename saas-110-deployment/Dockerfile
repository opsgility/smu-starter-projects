# Multi-stage build for the Lumen Trail API (Hono on Node 22).
# Used by SAAS-110 lab 4 (Cloud Run) and SAAS-115 lab 4 (Azure Container Apps).

FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json* ./
COPY apps/api/package.json ./apps/api/
RUN npm ci --omit=dev --workspace apps/api

FROM node:22-alpine AS build
WORKDIR /app
COPY package.json package-lock.json* ./
COPY apps/api/ ./apps/api/
RUN npm ci --workspace apps/api
RUN npm --workspace apps/api run build

FROM node:22-alpine AS runtime
WORKDIR /app
ENV NODE_ENV=production
ENV PORT=8080
COPY --from=deps /app/node_modules ./node_modules
COPY --from=deps /app/apps/api/node_modules ./apps/api/node_modules
COPY --from=build /app/apps/api/dist ./apps/api/dist
COPY apps/api/package.json ./apps/api/package.json
EXPOSE 8080
CMD ["node", "apps/api/dist/index.js"]
