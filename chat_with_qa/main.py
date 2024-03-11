from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from app.config.database import engine
from app.models import app_models
from app.routes import users_routes
import uvicorn

app_models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ChatWithQA",
    description="It gives answer related to software testing",
    contact={
        "name": "Kunal Katariya",
        "email": "kunal.katariya@yash.com"
    }
)

app.include_router(users_routes.router)

@app.get("/")
async def root():
    return {"message": "Hello world"}

# CORS Middleware to allow requests from React app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=7000,
        reload=True
    )

