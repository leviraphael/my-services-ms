from fastapi import FastAPI

app = FastAPI()


@app.get("/",status_code=200)
def root():
    return {"200"}
