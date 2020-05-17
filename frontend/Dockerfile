FROM node:12.16.3-alpine3.9
WORKDIR /code
COPY package.json package-lock.json ./
RUN npm install --quiet
COPY . .
