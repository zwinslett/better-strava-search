# Better Strava Search (WIP)

This is an attempt to build a better search interface for **running** activites on Strava using
[Apache Solr](https://solr.apache.org/) and [Django Rest Framework](https://www.django-rest-framework.org/).

Strava's native activity search, especially on web, is exceedingly limited. By taking advantage of the
[Strava API](https://developers.strava.com), this program stores **running** activities in a SQLite database and indexes
each activity in Solr, giving the user full access to Solr's robust searching capabilities against their activities.
While Solr already supports REST-like search operations using HTTP methods, Django RF provides a highly configurable way
to manage search requests to Solr in a truly RESTful API. Django also provides a framework for UI development to help
abstract Solr's syntax away from the user. 

## What's done
- A script for requesting data from Strava and saving it to a SQLite database
- A script for ingesting data from SQLite into Solr. 
- Defined SQLite and Solr schemas
- A model, serializer and view for an endpoint that supports `field` and `q` parameters which queries Solr against those parameters and returns the matching activities. 

## What's not done
- A basic user interface for making queries without needing Solr syntax in the `q` param. 
- A vector-based similarity score on activities.

## How to run this program 
In order to run this program, you'll need: 

- A Strava account.
- At least one activity recorded on that Strava account and one saved piece of gear associated with that activity. 
- A personal API application on that Strava account. 
  - and the corresponding `client_id`, `client_secret` and `refresh_token` for that API application.

Below instructions are provided for creating a personal API application and retrieving the necessary values to run this program. 
Please note that, in the settings for your personal API application, you will find a refresh token; however, that is not a substitute
for the steps below describing how to retrieve a refresh token for use by this program. The token provided in the settings page for your personal application
only has read access, and this program requires a token with read all access.

### How to get client_id and client_secret

- Create an API Application on Strava at [https://www.strava.com/settings/api ](https://www.strava.com/settings/api) and
  set the Authorization Callback Domain to localhost
- Navigate back to [https://www.strava.com/settings/api ](https://www.strava.com/settings/api) and you should see Client
  ID, Client Secret, Your Access Token, and Your Refresh Token

### How to request a refresh_token

- Replace the values in the following template with the appropriate values from your API application's settings page and navigate to the URL in a browser: `https://www.strava.com/oauth/authorize?client_id=[your_client_id]&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:read_all`
- Copy the code provided in the URL after authorizing your app. The URL should look like
  this: `http://localhost/exchange_token?state=&code=[CODE]&scope=read,activity:read_all`
- Make the following GET request either from the commandline or a GUI like Postman or HTTPie:

````
curl --request POST \
  --url 'https://www.strava.com/oauth/token?client_id=[your_client_id]&client_secret=[your_client_secret]&code=[CODE]&grant_type=authorization_code'
````

- Your refresh token will be in the response as `"refresh_token"`

### How to add these values to the program
Once you have your `refresh_token`, `client_secret` and `client_id` ready, you can either replace the values
in the payload array with your values or add them to the `login.example.py` file and remove the "example" from the 
file name. The login file is imported in the appropriate files and its values are inserted into the payload
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
### Dependencies 
- Docker for running the docker-compose file and containerized Solr. 
- The Python dependencies in the requirements.txt

### Getting started
Once your Strava API application is set up and the proper authentication steps are taken, the next step is to set up your database and Solr core. If you're using SQLite, the schema is defined in the schema.sql file. If you decide to use a different database, you'll need to define the schema you'd like and update the `strava_ingest.py` file to accommodate any changes to the column names etc. 

Setting up a Solr core is relatively simple. If you'd prefer to use a GUI instead of the CLI, run `docker-compose up` and use the Solr admin to create a new core. You can read more [in Apache's documentation](https://solr.apache.org/guide/solr/latest/index.html). As far defining your Solr schema, it should be completely hands-off. The `solr_ingest.py` file assumes the use of Solr's [dynamic fields](https://solr.apache.org/guide/solr/latest/indexing-guide/dynamic-fields.html). The TLDR is you should not have to define the fields in Solr's schema explicitly if you do not make changes to the database columns or `solr_ingest.py`. Even if you do make changes to the database, you can still leverage dynamic fields by following the conventions. 

Once you've finished setting up your database and Solr core, you can simply add them to `env.example.py` and remove "example" from the file name. `env.py` is imported in the necessary files where these values are needed. 

Now that everything is configured correctly, you should run `strava_ingest.py` and `solr_ingest.py` in that order. The `strava_ingest.py` files can be configured to fetch activities between two dates. Note that before running `solr_ingest.py` you should have Solr running (`docker-compose up`). 

If everything works as intended, your database and Solr core should have rows and documents respectively for each activity within the defined date range of your Strava ingest. You can now start Django and Solr, if it's not still running, and navigate to `api/activities/search/` on your local. You're ready to search against your activities. Here's an example: 

`/api/activities/search/?q=*ASICS*&field=gear_name_s`

As you can see, the search is still dependent on Solr's syntax. A feature goal of this search interface is incorporating a GUI for search that abstracts away Solr's syntax. 