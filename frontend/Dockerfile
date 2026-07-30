# 构建阶段
FROM node:20 AS build

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

RUN chmod -R +x node_modules/.bin

RUN npm run build-only

# 运行阶段
FROM nginx:stable-alpine

# Install curl for healthcheck
RUN apk add --no-cache curl

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
