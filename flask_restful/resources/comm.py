from flask_restful import Resource
import os


class Comm(Resource):
    
    def get(self, job_id): 
        print(job_id) 
        pass

    def post(self, job_id, task): 
        print("--------Post to comm--------")
        print (job_id)        
        os.system(task["task"])
        return job_id, task, 201

        