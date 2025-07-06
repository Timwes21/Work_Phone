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

RUN npm run build


RUN npx vite build --config config/vite.config.ts


CMD ["npm", "npx", "vite", "preview"]
