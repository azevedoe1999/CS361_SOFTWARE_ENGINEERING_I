// Package main provides a simple API that fetches a random developer joke
// from an external API and returns it as JSON.
//
// ## Overview
// This API exposes a single endpoint `/quote` which fetches a random developer joke
// from the Chuck Norris API (https://api.chucknorris.io).
//
// ## Usage
// - Start the server by running the Go application.
// - Access the `/quote` endpoint with a GET request to receive a JSON response containing the joke.
//
// ## Example Response
// ```json
//
//	{
//	    "value": "Chuck Norris can write infinite loops in finite time."
//	}
//
// ```
package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
)

// Joke represents the structure of the response from the external API.
// The API returns a JSON object where `value` contains the joke text.
type Joke struct {
	Value string `json:"value"`
}

func main() {
	// Start the HTTP server and register the /quote endpoint.
	http.HandleFunc("/quote", quoteHandler)

	fmt.Println("Server started at http://localhost:8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

// quoteHandler handles requests to the /quote endpoint.
// It fetches a random developer joke from an external API and returns the response
// as JSON.
//
// ## Endpoint
// - **Method**: GET
// - **URL**: `/quote`
//
// ## Responses
// - **200 OK**: Returns a JSON object with the joke.
// - **405 Method Not Allowed**: If a non-GET method is used.
// - **500 Internal Server Error**: If the external API fails.
//
// ## Example Request
// ```bash
// curl -X GET http://localhost:8080/quote
// ```
//
// ## Example Response
// ```json
//
//	{
//	    "value": "Chuck Norris can divide by zero."
//	}
//
// ```
func quoteHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Only GET method is allowed", http.StatusMethodNotAllowed)
		return
	}

	quote, err := fetchJoke()
	if err != nil {
		http.Error(w, "Failed to fetch quote", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	if err := json.NewEncoder(w).Encode(quote); err != nil {
		http.Error(w, "Failed to encode response", http.StatusInternalServerError)
	}
}

// fetchJoke retrieves a random developer joke from the Chuck Norris API and unmarshals it into a Joke struct.
//
// ## External API
// - URL: https://api.chucknorris.io/jokes/random?category=dev
//
// ## Returns
// - A `Joke` object containing the joke text.
// - An error if the request fails or the JSON cannot be parsed.
func fetchJoke() (*Joke, error) {
	resp, err := http.Get("https://api.chucknorris.io/jokes/random?category=dev")
	if err != nil {
		return nil, fmt.Errorf("failed to fetch joke: %w", err)
	}
	defer resp.Body.Close()

	var joke Joke
	if err := json.NewDecoder(resp.Body).Decode(&joke); err != nil {
		return nil, fmt.Errorf("failed to parse JSON: %w", err)
	}

	return &joke, nil
}
