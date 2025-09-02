FROM node:24

WORKDIR /app

RUN npm install tailwindcss @tailwindcss/cli

COPY css ./css
COPY static ./static
COPY templates ./templates

CMD ["npx", "@tailwindcss/cli", "-i", "./css/input.css", "-o", "./static/output.css"]
