FROM node:26-alpine AS development-dependencies-env
COPY . /app
WORKDIR /app
RUN npm ci

FROM node:26-alpine AS production-dependencies-env
COPY ./package.json package-lock.json /app/
WORKDIR /app
RUN npm ci --omit=dev

FROM node:26-alpine AS build-env
COPY . /app/
COPY --from=development-dependencies-env /app/node_modules /app/node_modules
ENV VITE_API_BASE_URL=http://localhost:5001/api/web/v1
WORKDIR /app
RUN npm run build

FROM node:26-alpine AS dev
COPY . /app
WORKDIR /app
RUN npm install
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]

FROM node:26-alpine
RUN apk add --no-cache curl
COPY ./package.json package-lock.json /app/
COPY --from=production-dependencies-env /app/node_modules /app/node_modules
COPY --from=build-env /app/build /app/build
WORKDIR /app
EXPOSE 5000
CMD ["npm", "run", "start"]
