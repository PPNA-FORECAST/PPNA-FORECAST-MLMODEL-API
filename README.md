# PPNA FORECAST API

PPNA Forecast is a API to interact with PPNA Forecast frontend. It is used for authentication, authorization, interact with google engine and PPNA Forecastin machine learning model. 


#### Features
 - Logic for interact with google earth engine 
 - Logic for interact with ppna forecasting ml model
 - Embebed MongoDB 
 - Token-Based Authentication (Adjust lifetime from within app.py)


A quick rundown of the actions included can be seen in the following table:

| **Action** |            **Path**           |                     **Details**                    |
|:----------:|:-----------------------------:|:--------------------------------------------------:|
|    POST    |           /api/v1/users       |                 Register a User                    |
|     GET    |           /api/v1/user        |                 Get Users                          |
|    POST    |           /api/v1/login       |                 Login to the API                   |




 ## Run it
It is a Flask application so in order to run it you can install all requirements and then run the `app.py`.
To install all requirements simply run `pip3 install -r requirements.txt` and then `python3 app.py`.

Or if you prefer you can also run it through docker or docker compose.

 #### Run it through Docker

~~~~
docker-compose up -d
~~~~

### Project Structure 

https://auth0.com/blog/best-practices-for-flask-api-development/