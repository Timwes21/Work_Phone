FROM node:20

WORKDIR /frontend

COPY . .

RUN npm install

EXPOSE 5173  # or whatever your dev server port is

CMD ["npm", "run", "dev"]
