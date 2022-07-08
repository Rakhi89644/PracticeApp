#import re
from curses.ascii import US
from doctest import Example
from itertools import product
from urllib import request
from fastapi import FastAPI,HTTPException,Request
#from uuid import UUID
from typing import Counter, List,Optional
from h11 import PRODUCT_ID
from pydantic import BaseModel,Field
from starlette.responses import JSONResponse

class NegativeNumberException(Exception):
    def __init__(self,product_to_return):
        self.product_to_return = product_to_return



app = FastAPI()

class User(BaseModel):
    id:int
    title:str = Field(min_length=1)
    description:Optional[str] = Field(title="Description of the product",
                                          max_length=100,min_length=1)
    rating:int = Field(gt=-1,lt=6)

    class Config(BaseModel):
        schema_extra = {
            "example":{
                "id":107,
                "title":"QCdefault",
                "description":"QCdefault product",
                "rating":4
            }
        }
# exclude the rating to the product
class ProductNoRating(BaseModel):
    id:int
    title:str = Field(min_length=1)
    description:Optional[str] = Field(
        None,title="description of the product",
        max_length=100,
        min_length=1
    )

Products = []

@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request:Request,exception:NegativeNumberException):
    return JSONResponse(
        status_code = 418,
        content={"message":f"Hey,how do you want the {exception.product_to_return}"}

    )

@app.get("/product/{id}")
async def read_product():
    for x in Products:
        if x.id == id:
            return x
    raise raise_item_exception()

@app.get("/product/rating",response_model=ProductNoRating)
async def read_product_no_rating():
    for x in Products:
        if x.id == id:
            return x
    raise raise_item_exception()


@app.get('/product')
async def read_all_user(product_to_return:Optional[int]=None):
    if product_to_return and product_to_return > 0:
        raise NegativeNumberException(product_to_return=product_to_return)
    if len(Products) < 1:
        create_product()
    if product_to_return and len(Products) >= product_to_return:
        i=1
        new_product =[]
        while i <=product_to_return:
             new_product.append(Products[i-1])
             i+=1
             return new_product
    return Products


            

@app.post('/')
async def create_user(user:User):
    Products.append(user)
    return Products

# update the product
@app.put("/")
async def update_user():
    Counter = 0
    for x in Products:
        Counter +=1
        if x.id == id:
            Products[Counter -1] = User
            return Products

@app.delete('/')
async def delete_book():
    Counter = 0
    for x in Products:
        Counter +=1
        if x.id == id:
            del Products[Counter -1]
            return f'ID:{id} deleted'
    raise raise_item_exception()

def create_product():
    product_1 = User(id=101,title="KalyanJwell",description="first product",rating=3)
    product_2 = User(id=102,title="Vistara",description="second product",rating=3)
    product_3 = User(id=103,title="e-gift",description="third product",rating=4)
    product_4 = User(id=104,title="KalyanGold",description="fivth product",rating=5)

    Products.append(product_1)
    Products.append(product_2)
    Products.append(product_3)
    Products.append(product_4)

def raise_item_exception():
    return HTTPException(status_code=404,
    detail="Product does not found",
    headers={"X-Header_Error":"Nothing details found"})



    