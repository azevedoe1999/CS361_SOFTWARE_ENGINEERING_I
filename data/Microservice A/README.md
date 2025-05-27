# microserviceA
--
Package main provides a simple API that fetches a random developer joke from an
external API and returns it as JSON.

## Overview This API exposes a single endpoint `/quote` which fetches a random
developer joke from the Chuck Norris API (https://api.chucknorris.io).

## Usage - Start the server by running the Go application. - Access the `/quote`
endpoint with a GET request to receive a JSON response containing the joke.
```
curl -X GET http://localhost:8080/quote
```


## Example Response: json

```
    {
        "value": "Chuck Norris can write infinite loops in finite time."
    }

```


## UML Diagram:
```
User/Client          Go API Server          External API
     |                     |                     |
     |---- GET /quote ---->|                     |
     |                     |                     |
     |                     |--- fetchJoke() --->|
     |                     |                     |
     |                     |<--- JSON Response --|
     |                     |                     |
     |<-- JSON Response ---|                     |
     |                     |                     |
```


## Team Communication Contract:
![alt text](coummincation_contract.png)