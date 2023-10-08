from fastapi import FastAPI, HTTPException
from EndPoint.apis import NBResponse, AMRequest, NBRequest

app = FastAPI()


@app.post("/search", response_model=NBResponse)
async def root(item: AMRequest):
    print(item)
    nb = NBRequest(item.slug, item.token)
    next = None
    results = []
    while True:
        resp = nb.search(item.since, next)
        if resp.status_code == 200:
            results += resp.json()['results']
            next = resp.json()['next']
            if next is None:
                break
        else:
            break


    return NBResponse(message=f'{len(results)} people returned')

@app.get("/person")
async def person(id: int, slug: str, token: str):
    nb = NBRequest(slug, token)
    try:
        person = nb.getPerson(id).json()['person']
    except:
        raise HTTPException(status_code=404, detail="Person not found")
    return NBResponse(message=f'{person["first_name"]} {person["last_name"]} returned')