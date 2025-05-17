# build frontend
FROM node:20-slim AS build
WORKDIR /app
COPY tokenblood/package*.json ./
RUN npm ci # install dependencies
COPY tokenblood/. .
RUN npm run build

# Build nginx to deliver static files
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"] 