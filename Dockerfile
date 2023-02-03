FROM node:12

WORKDIR /

COPY package*.json ./

RUN npm install

RUN apt update && apt install python3-pip -y

RUN pip3 install requests

COPY . .

ENV PORT=13800

EXPOSE 13800

CMD ["npm", "start"]

