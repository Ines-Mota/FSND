# Trivia API

The following document aims to provide a user's guide to the Trivia API. This API is used to play a game of trivia, you can pick categories, play with random questions and add new questions!


# Getting Set up

Before using the Trivia API there are a few steps to be taken in order to get it up and running.
In the `\backend\flaskr`  you will find the main file for using the app:
>`__ini__.py`

In the backend folder, you will also find `models.py` -  which contains the connection details and object representation in the database of the main entities of the project (in this case the categories and questions) -,and `test_flaskr.py` where the tests for the API are run.

The frontend set up has not been change, so to get it up and running you can follow the provided instructions for this project.
## Frontend

1.  **Installing Node and NPM**  
    This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from  [https://nodejs.com/en/download](https://nodejs.org/en/download/).
    
2.  **Installing project dependencies**  
    This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the  `frontend`  directory of this repository. Open the terminal and run:
```html
npm install
```

## Backend
### Installing Dependencies for the Backend

1.  **Python 3.7**  - Follow instructions to install the latest version of python for your platform in the  [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)
    
2.  **PIP Dependencies**  - Once you have your virtual environment setup and running, install dependencies by navigating to the  `/backend`  directory and running:

```
pip install -r requirements.txt
```
This will install all of the required packages we selected within the  `requirements.txt`  file.

5.  **Key Dependencies**

-   [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.
    
-   [SQLAlchemy](https://www.sqlalchemy.org/)  is the Python SQL toolkit and ORM we'll use to handle the lightweight sqlite database.
    
-   [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#)  is the extension we'll use to handle cross origin requests from our frontend server.
    

### Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in Windows command line run:
```
> psql -U yourUsername -d triviadb -a -f trivia.psql
```
Do equivalent for Linux and Mac.

The database name should be 'triviadb', however you should adapt the username and password for your own server and make sure those match the ones defined in models.py and test.py in order to successfully run the app.
```
database_name = "triviadb"
database_path = "postgresql://{}:{}@{}/{}".format('yourUsername','yourPassword','localhost:5432', database_name)
```
### Running the server

On Windows command line run the following commands (make sure you are in the correct directory to run the app).
```
>set flask_app=__init__.py
>set flask_env=development
>set flask_debug=true
>flask run
```
Do the equivalent for linux or mac.


# Endpoints 

In the table below you can find the endpoints available along with its description

|      Request          |Endpoint                       |Description                         |
|----------------|-------------------------------|-----------------------------|
|GET			|`/categories`            |Gets all of the categories available           |
|GET         |`/questions`            |      Requests a list of questions  |
|DELETE        |`/questions/<int:question_id>`|Deletes existing question|
|POST      |`/questions`|Adds new question|
|POST      |`/search`|Finds question from given search term|
|GET      |`/categories/<int:cat_id>/questions`|Gets questions from a given category|
|POST      |`/quizzes`|Returns questions from a chosen category or randomly to play the quiz|


# Payloads

Bellow are shown the expected payloads from the previously presented requests.

```html
GET - http://localhost:5000/categories
```
```html
#Returns

{
"categories": {
	"1": "Science",
	"2": "Art",
	"3": "Geography",
	"4": "History",
	"5": "Entertainment",
	"6": "Sports"
},
"success": true
}
```


------------------
```html
GET - http://localhost:5000/questions?page=1
```
```html
#Returns

{
	"Success": true,
	"categories": [
		"Science",
		"Art",
		"Geography",
		"History",
		"Entertainment",
		"Sports"
		],
"questions": [
	{
		"answer": "Apollo 13",
		"category": 5,
		"difficulty": 4,
		"id": 2,
		"question": "What movie earned Tom Hanks his third straight Oscar 		nomination, in 1996?"
	}
	],
"totalQuestions": 29

# Note: This endpoint returns a list of 10 questions per page, but in order to keep the doc simple only one is shown in the example
```
------
```html
DELETE - http://localhost:5000/questions/1
```
```html
#Returns

{
"success": true
}
```
---

```html
POST - http://localhost:5000/questions
```
```html
#Input data

{
	question: "Who won the FIFA world cup in 2010?",
	answer: "Spain",
	difficulty: 1,
	category: 6
}
```
```html
#Returns

```html
#Input data

{
	"answer": "Spain",
	"category": 6,
	"difficulty": 1,
	"question": "Who won the FIFA world cup in 2010?",
	"success": true
}
```
---
```html
POST - http://localhost:5000/search
```
```html
#Input data

{
"searchTerm": "which"
}
```
```html
#Returns

{
"questions": [
{
	"answer": "The Palace of Versailles",
	"category": 3,
	"difficulty": 3,
	"id": 14,
	"question": "In which royal palace would you find the Hall of Mirrors?"
},
{
	"answer": "Agra",
	"category": 3,
	"difficulty": 2,
	"id": 15,
	"question": "The Taj Mahal is located in which Indian city?"
}
],
	"success": true,
	"totalQuestions": 2
}
```
---
```html
GET - http://localhost:5000/categories/1/questions
```
```html
#returns

{
	"currentCategory": "Science",
	"questions": [
	{
	"answer": "The Liver",
	"category": 1,
	"difficulty": 4,
	"id": 20,
	"question": "What is the heaviest organ in the human body?"
},
{
	"answer": "Alexander Fleming",
	"category": 1,
	"difficulty": 3,
	"id": 21,
	"question": "Who discovered penicillin?"
},
{
	"answer": "Blood",
	"category": 1,
	"difficulty": 4,
	"id": 22,
	"question": "Hematology is a branch of medicine involving the study of what?"
},
{
	"answer": "Spain",
	"category": 1,
	"difficulty": 1,
	"id": 52,
	"question": "Who won the FIFA world cup in 2010?"
}
],
	"success": true,
	"totalQuestions": 4
}
```
---
```html
POST - http://localhost:5000/quizzes
```
```html
#Input data

{
"previous_questions": [],
"quiz_category": {"type": "click", "id": 0 }
}
```
```html
#Returns

{
	"question": {
		"answer": "Agra",
		"category": 3,
		"difficulty": 2,
		"id": 15,
		"question": "The Taj Mahal is located in which Indian city?"
		},
	"success": true
}
```
# Response Status Codes


|     Status Code  |     Description                         |
|------------------|-----------------------------------------|
|200			   | OK - The request was successful!      |
|400			   | Bad request - the server cannot or will not process the request due to something that is perceived to be a client error      |
|404               |  Not Found - The requested resource could not be found.          |
|405			   | HTTP method is not allowed      |