import uvicorn
from fastapi import FastAPI
from router import step1, step2, step3
import models
from database import engine
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
app.include_router(step1.router)
app.include_router(step2.router)
app.include_router(step3.router)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
