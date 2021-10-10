from flask_restful import Resource
from flask_restful.resources.comm import comm

import threading
import schedule
import time


class click(Resource):
    def get(task):   
        pass
    def post(task, job_id):
        # Dejar cron corriendo        
        def job(task, job_id):
            print("I'm working on...task " "task")

        schedule.every().seconds.do(job)
        schedule.every().minutes.do(job)
        schedule.every().hours.do(job)
        schedule.every().days.do(job)
        schedule.every().weeks.do(job)
        schedule.run_pending()
        pass

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
        continuous_thread.start()
        return cease_continuous_run

    # Start the background thread
    stop_run_continuously = run_continuously()

    # Do some other things...
    time.sleep(10)

    # Stop the background thread
    stop_run_continuously.set()