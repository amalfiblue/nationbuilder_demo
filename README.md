# nationbuilder_demo
Demo of API Use to access NB emulating bubble

## Background

Bubble (bubble.io) is a nocode platform on which the Amalfination webapp has been built. This makes demonstrating API code difficult so the code in here spikes the various calls used within Amalfination.

Amalfination backends Nationbuilder in providing misceleaneous extra services/convenience services. As such its principal requirement is to synchronise voluneteers with Nationbuilder (signup etc. occurs in the Nationbuilder site).

For some sites webhooks are used as triggers to this process whereas in others the mechanism is based on a polling system which is the preferred approach by Nationbuilder given the deprecation of webhook support and variability in their reliability.

The polling system thus uses the Nationbuilder GET **/people/search** API call to fetch people records that have been updated/added since the last poll event. This API call is emulated here with the response being a simple count of returned people records.

In the bubble app this call is forked to either a call to create a new user or update an existing user. In both cases the called 'function' uses a Nationbuilder GET **/people/:id** to get full details of the passed person - in some cases the search call (at least historically) was incomplete.

Finally, when person details are updated on Amalfination they are pushed back to Nationbuilder using the PUT **/person/:id** API call.

## Framework

For convenience and because we are currently working with FastAPI it was used as a framework for this process.

Just to play around the 3 calls to this app are a post (search), get (person) and put (person).

## Authentication

The current system is using v1 of the API and simple bearer token authentication (similar to the Nationbuilder API page)
## Install and Run

Loosely the following is the process, your mileage may vary depending on your OS, etc. - ther emay be some other dependencies (python) to get started.

1. Clone repository (git clone https://github.com/amalfiblue/nationbuilder_demo.git)
2. cd nationbuilder_demo
3. pip install poetry
4. poetry install
5. uvicorn EndPoint.__main__:app --reload

Then go to http://127.0.0.1:8000/docs to test the various endpoints
