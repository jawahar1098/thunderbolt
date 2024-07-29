#Using node as base image
FROM node:20

#Creating a /app as a working directory
WORKDIR /app

#Copying the package.json to /app directory
COPY package.json /app

#copy all the content to /app directory
COPY . /app

#install all the frontend dependecies
#RUN npm install
RUN npm install --legacy-peer-deps

#running on port 3000
EXPOSE 3000

#executing the below command after the container started.
CMD ["npm", "run", "dev"]

