FROM node:19-alpine
EXPOSE 3000
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
CMD ["yarn", "run", "dev"]