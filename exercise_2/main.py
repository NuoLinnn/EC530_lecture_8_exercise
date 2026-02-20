from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

account_count = 0

class Account(BaseModel):
    account_name: str
    account_id: Optional[int] = None
    notes: Optional[str] = None


@app.post("/account")
async def create_account(account: Account):
    global account_count
    account_count += 1
    account.account_id = account_count

    return {
        "Account Name": account.account_name,
        "Account ID": account.account_id
    }