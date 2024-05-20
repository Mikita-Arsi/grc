import os


is_deploy = 1

if is_deploy:
    token = os.getenv("TOKEN")
    webhook_url = 'https://bot-wsd-li-33.amvera.io'
else:
    token = os.getenv("TOKEN")
    webhook_url = 'https://15be-46-242-8-167.ngrok-free.app'


DB = "postgresql://postgres:5432@176.119.147.78:5432/bot"
