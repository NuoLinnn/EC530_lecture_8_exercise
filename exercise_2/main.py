from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional


app = FastAPI()

account_id_count = 0       # increments account_id
accounts_db = {}        # track accounts by id
account_names = set()   # track account names

class Account(BaseModel):
    account_name: str
    notes: Optional[str] = None

class UpdateNotesRequest(BaseModel):
    notes: Optional[str] = None

@app.post("/account")
async def create_account(account: Account):
    # if account name exists, raise 409 error
    if (account.account_name in account_names):
        raise HTTPException(status_code=409, detail= "Error creating account: account name already exists.")
    
    # increment account_id
    global account_id_count
    account_id_count += 1

    # 
    account_data = {
        "account_id": account_id_count,
        "account_name": account.account_name,
        "notes": account.notes
    }

    accounts_db[account_id_count] = account_data
    account_names.add(account.account_name)
    return account_data

@app.get("/get_account_by_id/{account_id}")
async def get_account_by_id(account_id: int):
    # if account_id does not exxist, raise 404 error
    if account_id not in accounts_db:
        raise HTTPException(status_code=404, detail= "Account does not exist")
    
    return accounts_db[account_id]

@app.get("/get_notes_by_account_id/{account_id}")
async def get_notes_by_account_id(account_id: int):
    # if account_id does not exist, raise 404 error
    if account_id not in accounts_db:
        raise HTTPException(status_code=404, detail="Account does not exist")
    
    account = accounts_db[account_id]
    return {"notes": account["notes"]}

@app.put("/account/update_notes/{account_id}")
async def update_notes_by_account_id(account_id: int, new_notes: UpdateNotesRequest):
     # if account_id does not exist, raise 404 error
    if account_id not in accounts_db:
        raise HTTPException(status_code=404, detail="Account does not exist")
    
    account = accounts_db[account_id]
    account["notes"] = new_notes.notes

    return {"notes": account["notes"]}