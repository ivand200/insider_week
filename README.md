# sudo docker build -t insider .
# sudo docker run -it insider /bin/bash
# celery -A tasks.worker.celery worker -I INFO -B
# exit