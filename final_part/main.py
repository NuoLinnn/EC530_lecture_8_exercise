# For a user in exercise 2, save the data of exercise 1 as a note
# Start with the currently written logic from exercise 2

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
import requests

app = FastAPI()

# In-memory storage
next_account_id = 0
accounts_db: Dict[int, dict] = {}
account_names: set[str] = set()


# ---------- Models ----------

class AccountCreate(BaseModel):
    account_name: str
    notes: Optional[str] = None


class UpdateNotesRequest(BaseModel):
    notes: Optional[str] = None


# ---------- Helper Function ----------

def get_account_helper(account_id: int):
    account = accounts_db.get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account does not exist")
    return account


# ---------- Routes ----------

@app.post("/accounts", status_code=200)
async def create_account(account: AccountCreate):
    global next_account_id

    if account.account_name in account_names:
        raise HTTPException(
            status_code=409,
            detail="Account name already exists"
        )

    next_account_id += 1

    account_data = {
        "account_id": next_account_id,
        "account_name": account.account_name,
        "notes": account.notes
    }

    accounts_db[next_account_id] = account_data
    account_names.add(account.account_name)

    return account_data


@app.get("/accounts/{account_id}")
async def get_account(account_id: int):
    return get_account_helper(account_id)


@app.get("/accounts/{account_id}/notes")
async def get_account_notes(account_id: int):
    account = get_account_helper(account_id)
    return {"notes": account["notes"]}


@app.put("/accounts/{account_id}/notes/recalls")
async def update_account_notes(account_id: int, update: UpdateNotesRequest):
    account = get_account_helper(account_id)

    account["notes"] = update.notes
    return {"notes": account["notes"]}

## New section ##
# For a user in exercise 2, save the data of exercise 1 as a note
@app.put("/accounts/{account_id}/save_notes")
async def save_account_notes(account_id: int):
    account = get_account_helper(account_id)

    # Call the API (from Exercise 1)
    r = requests.get("https://api.fda.gov/drug/enforcement.json?count=openfda.manufacturer_name.exact&limit=5")

    # Print the URL and staus code to make sure the user is accessing the right place and has success.
    print("URL: ", r.url)
    print("Status Code: ", r.status_code)

    # Assign the JSON data
    data = r.json() 

    # Format notes
    notes_formatted = []
    for item in data.get("results", []):
        manufacturer_name = item.get("term")
        recall_count = item.get("count")
        notes_formatted.append(f"{manufacturer_name} has {recall_count} recalls.")

    all_notes = "\n".join(notes_formatted)

    account["notes"] = all_notes
    return {"notes": account["notes"]}
