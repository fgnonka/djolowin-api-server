from locust import HttpUser, task

class MyUser(HttpUser):
    @task
    def my_task(self):
        self.client.get("/playercard/api/cardrarity")
        