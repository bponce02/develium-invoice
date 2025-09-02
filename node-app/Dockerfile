FROM node:24

WORKDIR /node

RUN npm install tailwindcss @tailwindcss/cli

COPY . .

CMD ["npx", "@tailwindcss/cli", "-i", "./src/input.css", "-o", "./static/output.css", "--watch"]

