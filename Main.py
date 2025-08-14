from http.client import HTTPException
import fastapi as _fastapi
import Blockchain as blockchain


blockchain = blockchain.Blockchain()
app = _fastapi.FastAPI()

# Mining
@app.post('/mine_block/')
def mine_block(data:str):
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code = 400, 
                                      detail = "Invalid Block")
    block = blockchain.mine_block(data = data)
    return block    

# Get all block
@app.get('/blockchain')
def get_blockchain_data():
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code = 400,     
                                      detail = "Invalid Blockchain")
    chain = blockchain.chain
    return chain

# Get single block by index
@app.get('/blockchain/{index}')
def get_blockchain_data(index: int):
    if index < 0 or index >= len(blockchain.chain):
        raise HTTPException(status_code=404, detail="Block not found") # Validation
    return blockchain.chain[index]

# Transactions
@app.post("/create_transactions")
def insert_transactions(data:str):
    
    
    
    
    
@app.post("/save")
def save_chain():
    try:
        blockchain.save_chain()
        return {"saved": True, "length": len(blockchain.chain)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/load")
def load_chain():
    try:
        blockchain.load_chain()
        return {"loaded": True, "length": len(blockchain.chain)}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Blockchain file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


