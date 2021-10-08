from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import os

os.system("echo Hello from the other side!")

app = Flask(__name__)
api = Api(app)

TODOS = {
    'job1': {'task': 'php ass pich', 'time': '* * * * *'},
    'job2': {'task': '?????'},
    'job3': {'cosa': 'profit!'},
}

def abort_if_todo_doesnt_exist(job_id):
    if job_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(job_id))

parser = reqparse.RequestParser()
parser.add_argument('task')


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, job_id):
        abort_if_todo_doesnt_exist(job_id)
        return TODOS[job_id]

        # crontab -l 

    def delete(self, job_id):
        abort_if_todo_doesnt_exist(job_id)
        del TODOS[job_id]
        # borrar cron 

        return '', 204

    def put(self, job_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[job_id] = task
        # crear crontab

        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        job_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        job_id = 'todo%i' % job_id
        TODOS[job_id] = {'task': args['task']}
        return TODOS[job_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/crons')
api.add_resource(Todo, '/crons/<job_id>')


if __name__ == '__main__':
    app.run(debug=True)