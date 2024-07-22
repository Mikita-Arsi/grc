import os


is_deploy = os.getenv("IS_DEPLOY")
if is_deploy:
    token = os.getenv("TOKEN")
    webhook_url = os.getenv("HOST")
else:
    token = os.getenv("TEST_TOKEN")
    webhook_url = os.getenv("TEST_HOST")


DB = os.getenv("DB")
