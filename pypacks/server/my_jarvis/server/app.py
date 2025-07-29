from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from .auth import router as auth_router, MIDDLEWARE_KEY

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=MIDDLEWARE_KEY)
app.include_router(auth_router)

@app.get("/health")
def health():
    return "OK"