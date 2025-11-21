from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

users = {
    "mohsin": {"pin":1234, "balance":5000},
    "ali": {"pin":1111, "balance":3000},
    "hamza": {"pin":2222, "balance":10000}
}

class AuthRequest(BaseModel):
    name: str
    pin_number: int

class DepositRequest(BaseModel):
    name: str
    amount: int

class BankTransferRequest(BaseModel):
    sender_name: str
    sender_pin: int
    recipient_name: str
    amount: int

@app.get("/")
async def root():
    return {"message": "Bank API running"}

@app.post("/authenticate")
async def authenticate_user(auth_request: AuthRequest):
    user = users.get(auth_request.name)
    if not user or user["pin"] != auth_request.pin_number:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials"
        )
    return {"name": auth_request.name, "bank_balance": user["balance"]}

@app.post("/deposit")
async def deposit_amount(deposit_request: DepositRequest):
    user = users.get(deposit_request.name)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    user["balance"] += deposit_request.amount
    return {"name": deposit_request.name, "updated_bank_balance": user["balance"]}

@app.post("/bank-transfer")
async def bank_transfer(transfer_request: BankTransferRequest):
    sender = users.get(transfer_request.sender_name)
    recipient = users.get(transfer_request.recipient_name)

    if not sender or sender["pin"] != transfer_request.sender_pin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Sender Credentials"
        )
    
    if not recipient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipient not found"
        )

    if sender["balance"] < transfer_request.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient balance"
        )

    sender["balance"] -= transfer_request.amount
    recipient["balance"] += transfer_request.amount

    return {
        "message": "Transfer successful",
        "sender_updated_balance": sender["balance"],
        "recipient_updated_balance": recipient["balance"]
    }
