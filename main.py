from type_class.modelname import *
from typing import Optional
from fastapi import FastAPI

# FAST API
app = FastAPI()

@app.get("/")
async def root():
	return "FastAPI Root"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    with open(f'{file_path}', 'r') as fp:
        a = fp.read()
    return a

@app.get("/items/")
async def read_itme(skip=None, limit=10):
    return f"{skip} / {limit}"

@app.post("/itemtest/")
async def item_test(item:Item):
    return f"{item.name} / {item.age}/ asdsaddda"
