FROM node:lts-alpine3.18
EXPOSE 3000
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
# RUN npm run build
# FROM nginx:stable-alpine
# COPY --from=build /app/dist /usr/share/nginx/html
CMD ["npm", "run", "dev"]