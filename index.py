from  fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses  import PlainTextResponse
app=FastAPI()




@app.get("/")
async def first_msg():
    return PlainTextResponse("Welcom to coolguide.tech backend , If you came here by mistaken ,you can leave")

    


@app.get("/get_products/{product_name}")
async def read_item(product_name):
      return PlainTextResponse("You have requestied for this",product_name)
