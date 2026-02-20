from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str
    user_id: int
    text_notes: str | None = None

app = FastAPI()

users_db = {}

# create user
@app.post("/users/", response_model=User)
async def create_user(user: User):
    if user.user_id in users_db:
        raise HTTPException(status_code=409, detail="User already exists")

    users_db[user.user_id] = user
    return user


# add note to user
@app.post("/users/{user_id}/note")
async def make_note(user_id: int, note: str):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")

    users_db[user_id].text_notes = note
    return users_db[user_id]


# get user info
@app.get("/users/{user_id}", response_model=User)
async def retrieve_account(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")

    return users_db[user_id]