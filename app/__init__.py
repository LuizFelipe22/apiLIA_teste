from fastapi import FastAPI

app = FastAPI()


from app.routes.estabelecimentos import *
