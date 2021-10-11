from flask import Flask, Blueprint
from flask_restful import reqparse, abort, Api, Resource
from flask_restful.resources.comm import comm
from flask_restful.resources.scheduler import click

app = Flask(__name__)
#app.config.from_object(Config())
api_bp = Blueprint('api', __name__)
api = Api(app)

PEJX = {
    'job1': {'task': 'php ass pitch', 'time': '* * * * *', 'state': 'active'},
}

def abort_if_todo_doesnt_exist(job_id):
    if job_id not in PEJX:
        abort(404, message="Todo {} doesn't exist".format(job_id))

parser = reqparse.RequestParser()
parser.add_argument('task')
parser.add_argument('time')
parser.add_argument('state')

# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, job_id):
        abort_if_todo_doesnt_exist(job_id)
        return PEJX[job_id] 

    def delete(self, job_id):
        abort_if_todo_doesnt_exist(job_id)
        click.delete(job_id)
        del PEJX[job_id]
        return '', 204

    def put(self, job_id):
        args = parser.parse_args()
        task = {'task': args['task'],'time': args['time'], 'state': args['state']}
        PEJX[job_id] = task
        # Evaluacion de post
        #comm.eval(self, job_id, task)
        click.post(self, job_id, task)
        return task, 201        


# TodoList
# shows a list of all PEJX, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return PEJX

    def post(self):
        args = parser.parse_args()
        #job_id = int(max(PEJX.keys()).lstrip('todo')) + 1
        #job_id = 'todo%i' % job_id
        #PEJX[job_id] = {'task': args['task']}
        return PEJX, 201

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/crons')
api.add_resource(Todo, '/crons/<job_id>')
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8080, debug=True)

