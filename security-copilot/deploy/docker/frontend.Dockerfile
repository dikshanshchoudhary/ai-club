FROM node:22-alpine
WORKDIR /app
COPY web/package.json web/tsconfig.json web/next-env.d.ts ./
COPY web/app ./app
COPY web/tailwind.config.ts ./
RUN npm install
EXPOSE 3000

