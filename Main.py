from fastapi import FastAPI, Form, HTTPException
import fastapi as _fastapi
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from Blockchain import Transactions
import Blockchain as blockchain


blockchain = blockchain.Blockchain()
app = _fastapi.FastAPI()

class GetTransactions(BaseModel):
    id: str
    sender: str
    receiver: str
    amount: float


# Get all block
@app.get("/blockchain")
def get_blockchain_data():
    if not blockchain.is_chain_valid():
        raise HTTPException(status_code=400, detail="Invalid Blockchain")

    return {
        "index": len(blockchain.chain),
        "valid": True,
        "pending_count": len(getattr(blockchain, "pending_transactions", [])),
        "pending_transactions": getattr(blockchain, "pending_transactions", []),
        "chain": blockchain.chain,
    }
    
# Get single block by index
@app.get('/blockchain/{index}')
def get_blockchain_data(index: int):
    if index < 0 or index >= len(blockchain.chain):
        raise HTTPException(status_code=404, detail="Block not found") # Validation
    return blockchain.chain[index]


# Mining
@app.post('/mine_block/')
def mine_block(data:str):
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code = 400, 
                                      detail = "Invalid Block")
    block = blockchain.mine_block(data = data)
    return block    


# Transactions
@app.post("/create_transactions_form") #Ai to debug
def create_transactions_form(
    id: str = Form(..., description="Transaction ID, e.g. tx001"),
    sender: str = Form(..., description="Sender name, e.g. Alice"),
    receiver: str = Form(..., description="Receiver name, e.g. Bob"),
    amount: float = Form(..., description="Amount, e.g. 100"),
):
    trans = Transactions(
        transaction_id=id,
        sender=sender,
        receiver=receiver,
        amount=amount,
    )

    valid = blockchain.insert_transaction(trans)
    if not valid:
        raise HTTPException(status_code=400, detail="Invalid Transaction")

    return {
        "accepted": True,
        "size": len(getattr(blockchain, "pending_transactions", [])),   
    }


@app.post("/pending_transactions")
def get_pending_transactions():
     return {
        "pending_transactions": getattr(blockchain, "pending_transactions", []),
        "count": len(getattr(blockchain, "pending_transactions", [])),
    }

@app.post("/save")
def save_chain():
    try:
        blockchain.save_chain()
        return {"saved": True, "index": len(blockchain.chain)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/load")
def load_chain():
    try:
        blockchain.load_chain()
        return {"loaded": True, "index": len(blockchain.chain)}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Blockchain file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


