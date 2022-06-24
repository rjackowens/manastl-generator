## README
Simple web app to generate raffles for ManaSTL.

## Prerequisites
- Install Docker
- Verify Docker is running

## **Running Application**

    docker build . -t manastl && docker run -p 8080:8080 manastl

This command will build and start the Docker image on your local machine.

Website Link: [localhost:8080](localhost:8080)

## Future Development

 - General cleanup
 - Generate form entries for multiple users
 - Form validation
 - Store generated list entries in DB
