import os
from flask import Flask, request, abort, jsonify

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from random import randint

from sqlalchemy.sql.expression import null

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__, instance_relative_config=True)
  setup_db(app)
  CORS(app, resources={r"/api/*" : {"origins": '*'}})
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response): 
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
      response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
      return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    
    # Sends a request to get the list of categories
    
    categories = Category.query.all()
    formatted_categories = [cat.type for cat in categories]

   # Turns the list of categories into a dictionary with the id and corresponding category

    cat_dict={}
    
    for i in range(len(formatted_categories)):
      cat_dict[i+1]=formatted_categories[i]

    return jsonify({
      'success': True,
      'categories': cat_dict
    })


    '''
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''
 
  
  @app.route('/questions')
  def get_questions():
    
    # Handles the pagination - 10 questions per page

    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    # Orders the question by id and creates a list of formatted questions according to specification in models.py
     
    questions = Question.query.order_by(Question.id).all()
    formatted_questions = [question.format() for question in questions]
    categories = [question.category for question in questions]

    # Creates a dictionary of categories

    cat_id = set(categories)
    cat_id = list(cat_id)

    cat_id_dict = {}
    id_key=range(len(cat_id))
    
    for i in id_key:
      cat_id_dict[i]=cat_id[i]

  
    categorynames=Category.query.filter(Category.id.in_(cat_id_dict))
    formatted_cat=[category.type for category in categorynames]


    # Checks if there are any questions in the chosen categories - if not 404 error is returned

    if len(formatted_questions) == 0:
      abort(404)
     
    return jsonify({
      'Success': True,
      'questions': formatted_questions[start:end],
      'totalQuestions': len(formatted_questions),
      'categories': formatted_cat
      # currentCategory - we are not returning current category because this endpoint requests all of the questions regardless of category
      })


    '''
 @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):

    # finds the question to be deleted 

    question = Question.query.filter(Question.id==question_id).one_or_none()

    # If the question is not found a 404 error is returned

    if question is None:
      abort(404)


    else:
      question.delete()
      return jsonify ({
        'success': True
      })



  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def add_new_question():

    new = request.get_json()

    # From the json input, it creates a new question and inserts it into the database
  

    try:


      new_question = new.get('question', None)
      new_answer = new.get('answer', None)
      new_category = new.get('category', None)
      new_difficulty = new.get('difficulty', None)
  

      newQuestion = Question(new_question,new_answer,new_category,new_difficulty)
      newQuestion.insert()


      return jsonify({
        'success': True,
        'question':new_question,
        'answer': new_answer,
        'category': new_category,
        'difficulty': new_difficulty
      })

     # if the json is not properly formed a 400 error is returned

    except:
      abort(400)
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/search', methods=['POST'])
  def search_question():

# From the json input a keyword is created to store the 'searchTerm'
    searchTerm = request.get_json()
    keyword = searchTerm.get('searchTerm', None)

# A request is sent to find the questions which contain the keyword

    result = Question.query.filter(Question.question.contains(keyword))
    result_format = [question.format() for question in result]

# If there are no questions containg the keyword a 404 error is returned
    if len(result_format)==0:
      abort(404)
      
    return jsonify ({
      'success': True,
      'questions': result_format,
      'totalQuestions': len(result_format)
      # currentCategory - Since there can be questions from different categories containing the same keyword we chose not to return current category 

    })

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:cat_id>/questions', methods=['GET'])
  def get_questions_by_category(cat_id):

    catTotal = Category.query.all()

 # Checks if category exists - if not a 404 error is returned

    if cat_id<=0 or cat_id > len(catTotal):
      abort(404)

 # Matches the cat_id input to the category from the database - if there isno match a 404 error is returned
    cat = Category.query.filter(Category.id == cat_id)[0]

    if cat is null:
      abort(404)

 # Gets questions from chosen category 
    questions = Question.query.filter(Question.category==str(cat.id))
    formatted_questions = [question.format() for question in questions]

 # If there are no questions a 404 error is returned  
    if len(formatted_questions)==0:
      abort(404)


    return jsonify({
      'success': True,
      'questions': formatted_questions,
      'totalQuestions': len(formatted_questions),
      'currentCategory': cat.type
    })

  

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_random_question ():

    body = request.get_json()
    cat_total = Category.query.all()

    selectedCategory = body.get('quiz_category', None)
    previousQuestions = body.get('previous_questions', None)

  # If the category id is 0 then questions from all categories can be returned as long as they are not included in previousQuestions

    if selectedCategory['id'] == 0:

      questions = Question.query.filter(Question.id.notin_(previousQuestions))
      formatted_questions = [question.format() for question in questions]

# If there are no questions left to return a 404 error is raised
      if len(formatted_questions)==0:
        abort(404)


# If the category id isn't 0 the code will check whether the category exists or not
    else:

      cat = Category.query.filter(Category.type==selectedCategory['type'])[0]
      


      if cat.id in [obj.id for obj in cat_total]:

# If the category id exists a request is sent to find the questions from the chosen category that are not included  in 'previousQuestions'

        questions = Question.query.filter(Question.category==str(cat.id), Question.id.notin_(previousQuestions))
        formatted_questions = [question.format() for question in questions]

# If there are no questions left to return a 404 error is raised

        if len(formatted_questions)==0:
          abort(404)


# If the category id doesn't exist a 404 error is raised

      else:
        abort (404)
        
# A random function is used to select a random question from the list of formatted_questions

    returnQuestion_id = randint(0, len(formatted_questions)-1)
    returnQuestion = formatted_questions[returnQuestion_id]
    

    return jsonify({
      'success': True,
      'question': returnQuestion
    })
      

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'Not Found'
    }), 404

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'Bad Request'
    }), 400

  return app

    