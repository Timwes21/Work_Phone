FROM node:20

WORKDIR /

COPY . .

RUN npm install

RUN npx tsc -b config/tsconfig.json

RUN npx vite build --config config/vite.config.ts

EXPOSE 3000

CMD ["npx", "vite", "preview", "--host", "0.0.0.0"]
