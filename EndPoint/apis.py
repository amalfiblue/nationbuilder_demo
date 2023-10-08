from pydantic import BaseModel, root_validator, Field
from datetime import datetime
import httpx

class AMRequest(BaseModel):
    slug: str = Field(alias="slug")
    token: str = Field(alias="token")
    since: datetime = Field(alias="since")

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
    
    def search(self, since: datetime = None, next:str = None):
        if next:
            return self.get(next)
        else:
            return self.get('api/v1/people/search',{'updated_since':since.strftime("%Y-%m-%dT%H:%M:%SZ") if since else None, 'limit':100})
        
    def getPerson(self, person_id: int):
        return self.get(f"api/v1/people/{person_id}")
