# Altana AI Atlas - Brazil

## Overview

Welcome to the Altana AI Atlas - Brazil query service. This service allows users to query our database of Brazilian
companies. 

## Setup & Configuration

The following dependencies must be installed to run the application:
- **Python 3.9+**: This can be downloaded and installed from 
  [https://www.python.org/downloads/](https://www.python.org/downloads/).
- **Docker**: Docker is used to run this service within a container, isolated from the host machine. Docker
  can be downloaded and installed by following the instructions 
  at [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/).
- **Docker-compose**: Docker-compose is used to easily bring up the API service. It can be installed by following
  the instructions at [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/).

### Install Dependencies

After Python is installed, the dependencies for the project must be installed. They can be installed with 
the following command:

```shell
pip install -r requirements.txt
```

### Loading the Database

The database must be populated with data before it can be queried. The application provides a convenient 
command-line tool for importing CSV files into the database. This can be performed with the following command:

```shell
flask load path/to/data.csv
```

## Operation

The application container can be built and ran with the following command:

```shell
docker-compose up
```

## Querying the Database

Several endpoints are exposed which will allow users to query the database. 
Each endpoint returns a JSON response.

*Note that all response data is de-duplicated!*

### Status Codes

* **200**: Success response.
* **400**: Bad request. An error in the request format was made.
* **404**: Invalid endpoint was requested.
* **500**: Internal error occurred within the application.

### Operations

#### List All Companies Matching an Operator

This endpoint allows a user to query the database for companies matching a specified operator via querystring.

##### Request

###### Endpoint

```
GET http://localhost:8000/companies?operator={operator name}
```

###### Parameters

```
operator name (string): Operator name to search for companies with
```

##### Response

###### 200 (example)

```json
{
  "companies": [
    "JOSE MANOEL DE SOUZA SILVA & CIA LTDA - ME", 
    "LEANDRO CONSTRUCOES EIRELI  - ME"
  ]
}
```

###### 400

```json
{
  "error": "Bad request"
}
```

***

#### List All Companies Connected by Shared Operators

This endpoint allows a user to query the database for companies connected to another company by shared operator. This
endpoint accepts a company specified via querystring.

##### Request

###### Endpoint

```
GET http://localhost:8000/companies/connected?company={company name}
```

###### Parameters

```
company name (string): Company name to search companies connected to
```

##### Response

###### 200 (example)

```json
{
  "companies": [
    "2.0 HOTEIS 2013 III SPE LTDA.",
    "SAPHYR ADMINISTRADORA DE CENTROS COMERCIAIS LTDA. - EPP", 
    "2.0 HOTEIS RIO BRANCO LTDA."
  ]
}
```

###### 400

```json
{
  "error": "Bad request"
}
```

***

#### List All Operators Matching a Company

This endpoint allows a user to query the database for operators matching a specified company via querystring.

##### Request

###### Endpoint

```
GET http://localhost:8000/operators?company={company name}
```

###### Parameters

```
company name (string): Company name to search for operators with
```

##### Response

###### 200 (example)

```json
{
  "operators": [
    "MARGARETE MOURA AZEVEDO COSTA", 
    "MARIERCE MOURA DA SILVA", 
    "JOSE MARIA DA SILVA FILHO"
  ]
}
```

###### 400

```json
{
  "error": "Bad request"
}
```

## Troubleshooting

Note that some web browsers and programs will not handle automatic encoding of URLs. In this instance,
certain characters must be encoded to make accurate queries to the database. Most Chromium-based web browsers will
automatically encode the URLs, however cURL will not.

## Application Architecture & Design Considerations

### Concerns

1. Data. The first concern I had was the variety of data that may need to be handled. Numerous pieces of
data contained ampersands which are not easily handled with URL querystrings. This was handled by reading raw querystrings within the application and manually splitting out values from querystring keys. I could have swapped querystrings for path variables, eg. /companies/<company_name>/operators, and that would have handled ampersands better without requiring custom extraction code. If the requirements for the application were broader, eg. needing to support multiple query criteria, then I would have more strongly considered this path (no pun intended :))
2. Simplicity. I was careful to tread the line between "too simple" and "too complex". Given the project requirement
   that the application be simple, I chose to write code that would accomplish the needed tasks, not much more.
   * The SQLite database is not normalized. For simplicity, this fits the bill nicely. However, there is redundant
     data due to this and the database could be normalized to help with this.
3. Data size. The uncompressed CSV is ~1.9GB in size. This presented a few challenges...
   1. While travelling for Thanksgiving, I only had my weak laptop with me. 1.9GB didn't play well with my RAM :)
   2. While the code did not need to be performant, it also should not give a MemoryError while importing the data and 
      it does need to actually finish importing the data before the deadline (haha). Because of this, I turned to
      using generators, SQLAlchemy core, and batched inserts to speedily import the data without causing too 
      much of a memory headache.
4. Documentation. I would have loved to introduce Swagger document generation based on the endpoints defined in the API.

### Architecture

The application is written in Python using the Flask microframework. Python was chosen for its simplicity and robust
ecosystem that can be leveraged when creating web applications. Flask was chosen for its lightweight profile, 
simplicity, and ease of extensibility. SQLite was chosen for the database as it is highly portable and requires no setup on the users part.

Because of the way I wrote the Flask application, I was also able to leverage the integration between the CLI
library `Click` and Flask to aid in importing data from the CSV file into the SQLite database.
I was able to utilize the Company model class (linked to the Companies database table) to very easily parse and
insert CSV rows into the database. With Click, I was able to simply add a `load` command to the `flask` command,
creating a simpler and more straightforward CLI application for the user.

Regarding the SQLite database... it is very portable and requires no setup. However, it begins to lack in performance
as the size of the data it holds grows, and this was quite noticeable. Inserts, especially with indices, seem to
markedly increase the load operation time as the database grows. Select queries also took in the realm of ~1 minute to
complete once the full dataset was inserted into the database. Adding indices dropped that down to <1 second times. 

Lastly, the application is fronted with the [gunicorn](https://gunicorn.org/) WSGI application server to help 
scale to handle network requests and then containerized with Docker. Using Docker not only makes running the 
application easier for the user, but also isolates the entire application and its dependencies from the host system.

## Changelog

* 1.0.0 - Initial application

