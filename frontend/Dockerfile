# Use official Node image
FROM node:20

# Set working directory INSIDE the container
WORKDIR /app

# Copy package.json and package-lock.json first (better build cache)
COPY package*.json ./
RUN echo "PORT env: $PORT"

# Install dependencies
RUN npm install

# Copy everything else (your source code, config, etc.)
COPY . .

# Debug: confirm your files are there
RUN ls -la
RUN ls -la src/

RUN npm run build


EXPOSE 8080


CMD ["npm", "start", "vite preview", "preview", "vite"]
