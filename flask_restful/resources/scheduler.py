from flask_restful import Resource
from flask_restful.resources.comm import Comm
import threading
import schedule
import time


class Click(Resource):        

    def get(job_id):
        for thread in threading.enumerate(): 
            print(thread.name)
        #print(job_id)   
        return thread.name

    def delete(job_id):
        print(job_id)
        return  

    def post(self, job_id, task):            

        def background_job():
            print('Hello from the background thread')
            print(task["time"])
            Comm.post(self, job_id, task)

        schedule.every(5).seconds.do(background_job)
        schedule.every(5).minutes.do(background_job)
        schedule.every(5).hours.do(background_job)
        schedule.every(5).days.do(background_job)
        schedule.every(5).weeks.do(background_job)
        #schedule.run_pending()
        

        def run_continuously(interval=1):
            """Continuously run, while executing pending jobs at each
            elapsed time interval.
            @return cease_continuous_run: threading. Event which can
            be set to cease continuous run. Please note that it is
            *intended behavior that run_continuously() does not run
            missed jobs*. For example, if you've registered a job that
            should run every minute and you set a continuous run
            interval of one hour then your job won't be run 60 times
            at each interval but only once.
            """
            cease_continuous_run = threading.Event()

            class ScheduleThread(threading.Thread):
                @classmethod
                def run(cls):
                    while not cease_continuous_run.is_set():
                        schedule.run_pending()
                        time.sleep(interval)

            continuous_thread = ScheduleThread()
            continuous_thread.name = job_id
            continuous_thread.start()

            return cease_continuous_run

        # Start the background thread
        stop_run_continuously = run_continuously()

        # Do some other things...
        time.sleep(1)

        # Stop the background thread
        # stop_run_continuously.set()

        return task, job_id, 201