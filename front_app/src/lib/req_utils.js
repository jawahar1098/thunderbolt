// Imports.
import { browser } from "$app/environment";
import { goto } from "$app/navigation";
import { ENV_OBJ } from "$lib/env.js";


// ---------- Local Storage Helper Functions ---------- //

// Get a locally stored value from browser.
export function browserGet(key) {

    // If a browser instance is valid/exists.
    if(browser) {

        // Fetch the data value for the key from local storage.
        const item = localStorage.getItem(key);
        if(item) {
            return item
        }
    }

    // Return null if a valid browser instance is not found.
    return null;
}

// Set a local value in the browser.
export function browserSet(key) {

    // If a browser instance is valid/exists.
    if(browser) {

        // Set the data value for the key in the local storage.
        localStorage.setItem("jwt", key);
    }

    // Return null if a valid browser instance is not found.
    return null;
}


// ---------- Requests Helper Functions ---------- //

// Make a POST request, with a JWT token if one is present.
export async function postRequest(fetch, url, body) {

    // Try/Catch block for issues with the request.
    try {

        // Record values for request headers.
        let headers = {}

        // If a body is present as form data, convert it into JSON and attach the appropriate header.
        if(!(body instanceof FormData)) {
            headers["Content-Type"] = "application/json";
            body = JSON.stringify(body)
        }

        // Get the JWT token if one is present and attach the appropriate header.
        const token = browserGet("jwt");
        if(token) {
            headers["Authorization"] = token;
        }

        // Make a POST request with fetch.
        const response = await fetch(url, {
            method: "POST",
            credentials: "include",
            body,
            headers
        })


        // Return unauthorized param if a 401 status is received. 
        if(response.status === 401) {
            return {
                "authorized": false
            }
        } else if(response.status === 205 && url.includes("logout")) {
            // If a refresh status is present and URL contains logout.
            localStorage.removeItem("jwt");

        // Process the response data if a 200 status is received.
        } else if(response.status === 200) {

            // Try/Catch block to capture response data.
            try {

                // Return the data in JSON format.
                return await response.json();

            } catch(err) {

                // Log the error and throw an exception.
                if(ENV_OBJ.APP_MODE === "DEVELOPMENT") {
                    console.log(err);
                }

                throw {
                    message: "ERROR"
                };
            }

        }else if (response.status === 440){
            goto("/")
        } else {

            // Try/Catch block to capture response error.
            try {
                const data = await response.json();
                const error = data.message[0].messages[0];
                
                if(ENV_OBJ.APP_MODE === "DEVELOPMENT") {
                    console.log(error.message);
                };

                throw {
                    message: "ERROR"
                };
            } catch(err) {

                // Log the error and throw an exception.
                if(ENV_OBJ.APP_MODE === "DEVELOPMENT") {
                    console.log(err);
                }
                throw err;
            }
        }

    } catch(err) {

        // Log the error and throw an exception.
        if(ENV_OBJ.APP_MODE === "DEVELOPMENT") {
            console.log(err);
        }
        
        throw {
            message: "ERROR"
        };
    }
}

// Make a GET request, with a JWT token if one is present.
export async function getRequest(fetch, url) {

    // Try/Catch block for issues with the request.
    try {

        // Record values for request headers.
        let headers = {}

        // Get the JWT token if one is present and attach the appropriate header.
        const token = browserGet("jwt");
        if(token) {
            headers["Authorization"] = token;
        }

        // Make a GET request with fetch.
        const response = await fetch(url, {
            method: "GET",
            credentials: "include",
            headers,
        })


        // Return unauthorized param if a 401 status is received. 
        if(response.status === 401) {
            return {
                "authorized": false
            }
        } else if(response.status === 200) {
            // Process the response data if a 200 status is received.
            
            // Try/Catch block to capture response data.
            try {
                console.log(response,"------------")
                // Return the data in JSON format.
                return await response.json()

            } catch(err) {

                // Log the error and throw an exception.
                if(ENV_OBJ.APP_MODE === "DEVELOPMENT") {
                    console.log(err);
                }

                throw {
                    message: "ERROR"
                };
            }
        } else {

            // Try/Catch block to capture response error.
            try {
                const data = await response.json();
                const error = data.message[0].messages[0];

                if(ENV_OBJ.APP_MODE === "DEVELOPMENT") {
                    console.log(error.message);
                }
                
                throw {
                    message: "ERROR"
                };

            } catch(err) {

                // Log the error and throw an exception.
                if(ENV_OBJ.APP_MODE === "DEVELOPMENT") {
                    console.log(err);
                }
                
                throw {
                    message: "ERROR"
                };
            }
        }

    } catch(err) {

        // Log the error and throw an exception.
        if(ENV_OBJ.APP_MODE === "DEVELOPMENT") {
            console.log(err);
        }

        throw {
            message: "ERROR"
        };
    }
}