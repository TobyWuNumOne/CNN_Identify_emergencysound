# 多階段構建
# 階段 1: 構建
FROM node:18-alpine as build-stage

WORKDIR /app

# 安裝 pnpm
RUN npm install -g pnpm

# 複製 package 文件
COPY package*.json ./
COPY pnpm-lock.yaml* ./

# 安裝依賴
RUN pnpm install --frozen-lockfile

# 複製源代碼
COPY . .

# 構建應用
RUN pnpm build

# 階段 2: 生產
FROM nginx:alpine as production-stage

# 複製構建結果
COPY --from=build-stage /app/dist /usr/share/nginx/html

# 複製 nginx 配置
COPY nginx.conf /etc/nginx/nginx.conf

# 暴露端口
EXPOSE 80

# 啟動 nginx
CMD ["nginx", "-g", "daemon off;"]