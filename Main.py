import fastapi as _fastapi
import Blockchain as blockchain


blockchain = blockchain.Blockchain
app = _fastapi.FastAPI()

# Mining"
@app.post('/mine_block')
def mine_block(data:str):
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code = 400, 
                                      detail = "Invalid Block")
    block= blockchain.mine(data = data)
    
    return block    

@app.get('/get_blockchain')
def get_blockchain(data:str):
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code = 400,     
                                      detail = "Invalid Block")