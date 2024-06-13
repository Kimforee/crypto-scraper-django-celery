import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Job, Task
from .serializers import JobSerializer
from .tasks import scrape_coin_data, my_task
from crypto_scraper.celery import app

logger = logging.getLogger(__name__)

class StartScraping(APIView):
    def post(self, request):
        coins = request.data
        print("hello world")
        if not all(isinstance(coin, str) for coin in coins):
            return Response({"error": "Invalid input"}, status=status.HTTP_400_BAD_REQUEST)

        job = Job.objects.create()
        for coin in coins:
            task = Task.objects.create(job=job, coin=coin)
            logger.info(f"Queueing task for {coin}")
            print(f"Queueing task for {coin}")
            print("about to call the task !")
            scrape_coin_data.delay(task.id)
            print("calling the task done !")

        result = my_task.delay(3, 5)
        print("you better stop at :::::::::",result)
        print("after the test task")

        # app.send_task('crypto_scraper.tasks.test_task')
        return Response({"job_id": job.job_id}, status=status.HTTP_202_ACCEPTED)

class ScrapingStatus(APIView):
    def get(self, request, job_id):
        print("here inside status")
        try:
            job = Job.objects.get(job_id=job_id)
        except Job.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = JobSerializer(job)
        return Response(serializer.data, status=status.HTTP_200_OK)