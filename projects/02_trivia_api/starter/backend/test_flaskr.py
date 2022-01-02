import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path =  "postgresql://{}:{}@{}/{}".format('postgres','password','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question':'Which of Newton’s Laws states that ‘for every action, there is an equal and opposite reaction?' ,
            'answer': 'The third law of motion' ,
            'category': '1' ,
            'difficulty': 5
        }
        


        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            category = Category('Science')
            self.db.session.add(category)
            self.db.session.commit()
    
    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            self.db.session.execute('DROP TABLE public.questions, public.categories')
            self.db.session.commit()
            
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

#test for get_categories

    def test_get_categories(self):
        self.client().post('/questions', json = self.new_question)
        res=self.client().get('/categories')
        self.assertEqual(res.status_code, 200)


    def test_405_categories(self):
            self.client().post('/questions', json = self.new_question)
            res=self.client().post('/categories')
            self.assertEqual(res.status_code, 405)

#test for get_questions  

    def test_get_questions(self):

        question=self.client().post('/questions', json = self.new_question)

        res=self.client().get('/questions')
        self.assertEqual(res.status_code, 200)

    def page_not_found_when_question_nonexistent(self):

        res=self.client().get('/questions/10000')



#test for delete_question 

    def test_delete_questions(self):
        i=1
        while i < 10:
            self.client().post('/questions', json = self.new_question)
            i=i+1

        res=self.client().delete('/questions/5')
        self.assertEqual(res.status_code, 200)

    def test_404_if_deleted_question_doesNot_exist(self):

        res=self.client().delete('/questions/100')
        self.assertEqual(res.status_code, 404)



#test for new_question

    def test__create_new_questions(self):
        
         res=self.client().post('/questions', json = self.new_question)
         self.assertEqual(res.status_code, 200)

    def test_badRequest_create_new_questions(self):

        res=self.client().post('/questions')
        self.assertEqual(res.status_code, 400) 

        


#test for search_question

    def test_search(self):

        newquestion=self.client().post('/questions', json = self.new_question)
        res=self.client().post('/search', json={'searchTerm':'Which'})
        self.assertEqual(res.status_code,200)

    def test_search_notFound(self):

        res=self.client().post('/search', json={'searchTerm':'what'})
        self.assertEqual(res.status_code, 404)




#test for get_questions_by_category

    def test_get_questions_by_category(self):
        i=1
        while i < 5:
            a = self.client().post('/questions', json = self.new_question)
            i=i+1
        newquestion=self.client().post('/questions', json = self.new_question)
        res=self.client().get('/categories/1/questions')
        self.assertEqual(res.status_code, 200)



    def test_notFound_get_categ_questions(self):
            i=1
            while i < 10:
                a = self.client().post('/questions', json = self.new_question)
                i=i+1

            res=self.client().get('/categories/1000/questions')
            self.assertEqual(res.status_code, 404)


 #test for quiz


    def test_quiz(self):
        i=1
        while i < 10:
            a = self.client().post('/questions', json = self.new_question)
            i=i+1

        res = self.client().post('/quizzes', json={'quiz_category':{"type": "Science", "id": "1"}, 'previous_questions':[]})
        self.assertEqual(res.status_code, 200)

    def test_error_for_no_questions_left(self):
        i=1
        while i < 10:
            a = self.client().post('/questions', json = self.new_question)
            i=i+1
        
        allQuestions = Question.query.all()
        formatted_questions = [question.id for question in allQuestions]

        res = self.client().post('/quizzes', json={'quiz_category':{"type": "Science", "id": "1"}, 'previous_questions': formatted_questions})
        self.assertEqual(res.status_code, 404)

    def test_GetAll_ReturnsAll(self):
        i=1
        while i < 10:
            a = self.client().post('/questions', json = self.new_question)
            i=i+1
        
        allQuestions = Question.query.all()
        formatted_questions = [1,2,3]

        res = self.client().post('/quizzes', json={'quiz_category':{"type": "click", "id": 0}, 'previous_questions': formatted_questions})
        self.assertEqual(res.status_code, 200)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()