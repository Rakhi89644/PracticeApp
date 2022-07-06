#import re
from curses.ascii import US
from doctest import Example
from itertools import product
from fastapi import FastAPI,HTTPException
#from uuid import UUID
from typing import Counter, List,Optional
from pydantic import BaseModel, Field



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


Products = []

@app.get('/')
async def read_all_user(product_to_return:Optional[int]=None):
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
@app.put("/{id}")
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
    raise HTTPException(status_code=404,detail='Invalid entery')

def create_product():
    product_1 = User(id=101,title="KalyanJwell",description="first product",rating=3)
    product_2 = User(id=102,title="Vistara",description="second product",rating=3)
    product_3 = User(id=103,title="e-gift",description="third product",rating=4)
    product_4 = User(id=104,title="KalyanGold",description="fivth product",rating=5)

    Products.append(product_1)
    Products.append(product_2)
    Products.append(product_3)
    Products.append(product_4)



    