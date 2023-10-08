from pydantic import BaseModel, root_validator, Field
from datetime import datetime
from typing import Union
import httpx
from typing import Dict

class AMRequest(BaseModel):
    slug: str = Field(alias="slug")
    token: str = Field(alias="token")
    since: datetime = Field(alias="since")

class Address(BaseModel):
    address1: Union[str, None] = None
    city: Union[str, None] = None
    state: Union[str, None] = None
    zip: Union[str, None] = None
    
    
    def __str__(self):
        return f"\{'address': {self.model_dump_json(exclude_unset=True)}\}"
class AMPerson(BaseModel):
    external_id: Union[str, None] = None
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    email: Union[str, None] = None
    email: Union[str, None] = None
    phone: Union[str, None] = None
    home_address: Union[Address, None] = None
    note: Union[str, None] = None

def __str__(self):
    return "{'person':" + self.dump_model_json(exclude_unset=True) + "}"

class NBResponse(BaseModel):
    message: str = Field(alias="message")

class NBRequest():
    Accept: str = "application/json"
    Content_Type: str = "application/json"
    Authorization: str = "Bearer"
    url: str = Field(alias="url")
    headers: dict = Field(alias="headers")

    def __init__(self, slug: str, token: str):
        self.url = f"https://{slug}.nationbuilder.com"
        self.headers = {
            "Accept": self.Accept,
            "Content-Type": self.Content_Type,
            "Authorization": f"{self.Authorization} {token}"
        }

    def get(self, url_ext:str, params:dict = None):
        return httpx.get(f"{self.url}/{url_ext}", headers=self.headers, params=params)
    
    def put(self, url_ext:str, data:dict):
        return httpx.put(f"{self.url}/{url_ext}", headers=self.headers, json=data)
    
    def search(self, since: datetime = None, next:str = None):
        if next:
            return self.get(next)
        else:
            return self.get('api/v1/people/search',{'updated_since':since.strftime("%Y-%m-%dT%H:%M:%SZ") if since else None, 'limit':100})
        
    def getPerson(self, person_id: int):
        return self.get(f"api/v1/people/{person_id}")
    
    def putPerson(self, id: int, person: AMPerson):
        return self.put(f"api/v1/people/{id}?fire_webhooks=false", {'person':person.model_dump() })
