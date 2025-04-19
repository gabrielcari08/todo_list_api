from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def hello_fastapi():
    return {"message": "Hello!"}