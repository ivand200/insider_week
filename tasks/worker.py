from celery import Celery
from app.main import app
from database.models import db
from celery.schedules import crontab
import gspread
import pandas as pd
from app.creds import credentials

def make_celery(app):
    celery = Celery(app.import_name)
    celery.conf.update(app.config["CELERY_CONFIG"])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

app.config.update(CELERY_CONFIG={
    "broker_url": "redis://:bsIwj0mAE3zODIm3irCJjn4KVAfWDfBp@redis-18506.c299.asia-northeast1-1.gce.cloud.redislabs.com:18506"
})
celery = make_celery(app)

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Task to update data from google sheet
    # Executes every day at 9
    sender.add_periodic_task(
        crontab(minute=0, hour=9),
        test_table.s(),
    )


@celery.task
def cron_test():
    print("test")
    return "Check"


@celery.task
def test_table():
    """
    Task for update data from google sheet
    """
    gc = gspread.service_account_from_dict(credentials)
    sh = gc.open("Asset")
    worksheet = sh.sheet1
    dataframe = pd.DataFrame(worksheet.get_all_records())
    dataframe.columns = ["ticker", "date", "open", "high", "low", "close"]
    dataframe.to_sql("asset", con=db.engine, if_exists="replace", index=False)
    print(dataframe)
    return True