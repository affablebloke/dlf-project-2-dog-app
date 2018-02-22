
from node:9.5.0-alpine
COPY . /code/
WORKDIR /code
RUN npm install && npm run build
CMD ["npm", "run", "start"]
EXPOSE 3000