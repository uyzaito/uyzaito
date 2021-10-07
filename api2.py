from flask import Flask, request
from flask_restful import Resource, Api
from flask_restful import fields, marshal_with


app = Flask(__name__)
api = Api(app)



resource_fields = {
    'task':   fields.String,
    'uri':    fields.Url('todo_ep')
}

class TodoDao(object):
    def __init__(self, todo_id, task):
        self.todo_id = todo_id
        self.task = task

        # This field will not be sent in the response
        self.status = 'active'

class Todo(Resource):
    @marshal_with(resource_fields)
    def get(self, **kwargs):
        return TodoDao(todo_id='my_todo', task='Remember the milk')

if __name__ == '__main__':
    app.run(debug=True)