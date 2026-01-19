# Better Strava Search (WIP)

This is an attempt to build a better search interface for **running** activites on Strava using
[Apache Solr](https://solr.apache.org/) and [Django Rest Framework](https://www.django-rest-framework.org/).

Strava's native activity search, especially on web, is exceedingly limited. By taking advantage of the
[Strava API](https://developers.strava.com), this program stores **running** activities in a SQLite database and indexes
each activity in Solr, giving the user full access to Solr's robust searching capabilities against their activities.
While Solr already supports REST-like search operations using HTTP methods, Django RF provides a highly configurable way
to manage search requests to Solr in a truly RESTful API. Django also provides a framework for UI development to help
abstract Solr's syntax away from the user. 

## How to get client_id and client_secret

- Create an API Application on Strava at [https://www.strava.com/settings/api ](https://www.strava.com/settings/api) and
  set the Authorization Callback Domain to localhost
- Navigate back to [https://www.strava.com/settings/api ](https://www.strava.com/settings/api) and you should see Client
  ID, Client Secret, Your Access Token, and Your Refresh Token

## How to request a refresh_token

- Replace the values in the following template with the appropriate values from your API application's settings page and navigate to the URL in a browser: `https://www.strava.com/oauth/authorize?client_id=[your_client_id]&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:read_all`
- Copy the code provided in the URL after authorizing your app. The URL should look like
  this: `http://localhost/exchange_token?state=&code=[CODE]&scope=read,activity:read_all`
- Make the following GET request either from the commandline or a GUI like Postman or HTTPie:

````
curl --request POST \
  --url 'https://www.strava.com/oauth/token?client_id=[your_client_id]&client_secret=[your_client_secret]&code=[CODE]&grant_type=authorization_code'
````

- Your refresh token will be in the response as `"refresh_token"`

## How to add these values to the program
Once you have your `refresh_token`, `client_secret` and `client_id` ready, you can either replace the values
in the payload array with your values or add them to the `login.example.py` file and remove the "example" from the 
file name. The login file is imported in the main program and its values are inserted into the payload
via f-strings.


```
payload = {
    'client_id': f'{login.client_id}',
    'client_secret': f'{login.client_secret}',
    'refresh_token': f'{login.refresh_token}',
    'grant_type': "refresh_token",
    'f': 'json'
}
```