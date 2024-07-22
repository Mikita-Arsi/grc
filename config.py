import os


is_deploy = os.getenv("IS_DEPLOY")
if is_deploy:
    token = os.getenv("TOKEN")
    webhook_url = ''
else:
    token = os.getenv("TOKEN")
    webhook_url = ''


DB = os.getenv("DB")
