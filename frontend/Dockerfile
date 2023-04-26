FROM node:19-alpine3.17
EXPOSE 3000
WORKDIR /app
COPY package.json .
RUN npm install
RUN npm i esbuild
COPY . .
CMD ["yarn", "run", "dev"]