# Use official Node image
FROM node:20

# Set working directory INSIDE the container
WORKDIR /app

# Copy package.json and package-lock.json first (better build cache)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy everything else (your source code, config, etc.)
COPY . .

# Debug: confirm your files are there
RUN ls -la
RUN ls -la src/

RUN npx config/tsconfig.json


RUN npx vite build --config config/vite.config.ts

EXPOSE 4173

CMD ["npx", "vite", "preview", "--host", "0.0.0.0", "--port", "4173"]
