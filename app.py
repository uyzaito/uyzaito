from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
#from flask_apscheduler import APScheduler
from crontab import CronTab

import os
os.system("echo Hello from the other side!")

# set configuration values scheduler settings
#class Config:
#    SCHEDULER_API_ENABLED = True

# crear
app = Flask(__name__)
#app.config.from_object(Config())

api = Api(app)

# initialize scheduler
#scheduler = APScheduler()
# if you don't wanna use a config, you can set options here:
# scheduler.api_enabled = True
#scheduler.init_app(app)
#scheduler.start()


TODOS = {
    'job1': {'task': 'php ass pitch', 'time': '* * * * *'},
}

def abort_if_todo_doesnt_exist(job_id):
    if job_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(job_id))

parser = reqparse.RequestParser()
parser.add_argument('task')
parser.add_argument('time')



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
        #scheduler.delete_all_jobs
        return '', 204

    def put(self, job_id):
        args = parser.parse_args()
        task = {'task': args['task'],'time': args['time']}
        TODOS[job_id] = task

        # crear crontab
        #system_cron = CronTab(tabfile='/etc/crontab', user=False)
        #job = system_cron[0]
        #job.user != None
        #system_cron.new(command='task', user='root')
        job  = cron.new(command="task")
        job.setall("* * * * *")

        #def scheduledTask():
        #    os.system("task")
        #    print("This task is running every 5 seconds")
        #scheduler.add_job(id =(job_id), func = scheduledTask, trigger = 'cron', seconds = 5,  minute="*",  week="*", day_of_week="*")

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
    app.run(host = '0.0.0.0', port = 8080, debug=True)