# Nao-flask
An attempt to control a Nao robot via a Python back-end using the Flask framework.

# Required dependencies
* Nao SDK (I used 2.1.4.13)
* Flask library (http://flask.pocoo.org/)

Sidenote: Based on this tutorial http://flask.pocoo.org/


# How to use

### POST VERB

TO let the Nao say something, send a POST request to /say with `application_json` as the body data type. The text that the Nao robot needs to say has to be in a Json with `text` as its key:

```bash
curl -i -H "Content-Type: application/json" -X POST -d '{"text":"Hello, I am Nao!"}' http://localhost:5000/say
```

### GET VERB

To show an approach using the `GET` http verb, i created an `/ask/:textToAsk` endpoint. For example go to: `http://localhost:5000/ask/HelloHowAreYou`
