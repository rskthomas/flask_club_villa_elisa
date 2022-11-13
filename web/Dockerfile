FROM node:14.20

RUN mkdir /app

WORKDIR /app

COPY package.json ./
COPY vite.config.js ./

EXPOSE 5173

RUN npm install --only-dev
RUN npm install -D tailwindcss

CMD ["npm","run", "dev", "--", "--host"]
