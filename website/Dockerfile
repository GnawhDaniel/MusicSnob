FROM node:latest AS dev
COPY . /app
WORKDIR /app
RUN npm ci
CMD ["npm", "run", "dev"]

# ----------------------------------------------------------



FROM node:latest AS prod
COPY . /app/
WORKDIR /app
RUN npm ci && npm run build
EXPOSE 5000
CMD ["npm", "run", "start"]