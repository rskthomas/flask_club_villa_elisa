FROM node:14.20-slim

RUN mkdir /app

WORKDIR /app

COPY package.json ./
COPY vite.config.js ./

EXPOSE 5173

RUN npm install --only-dev

CMD ["npm","run", "dev", "--", "--host"]
