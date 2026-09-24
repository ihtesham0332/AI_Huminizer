# Use official Node.js image
FROM node:18-alpine AS base

# Set working directory
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm ci

# Copy the application code
COPY . .

# Build the Next.js application
RUN npm run build

# Start the production server
EXPOSE 3000
ENV PORT 3000
CMD ["npm", "start"]
