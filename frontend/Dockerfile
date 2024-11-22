# 构建阶段
FROM node:18-alpine as build-stage
WORKDIR /app

# 设置 npm 使用淘宝镜像
RUN npm config set registry https://registry.npmmirror.com

COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# 生产阶段
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"] 