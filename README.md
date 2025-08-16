# Blockchiain_assigment2
Source: 
https://www.geeksforgeeks.org/python/create-simple-blockchain-using-python
https://www.youtube.com/watch?v=G5M4bsxR-7E

This project implements a simplified blockchain with the following features:
- Transaction validation (prevents double spending)
- Mining with Proof-of-Work consensus
- Block creation and chain validation
- RESTful API built with **FastAPI**
- Interactive API documentation available via **Swagger UI*

How to run:
- You will need to install the require library for this. To that copy and paste the text below into your terminal.: 
    - pip install -r requirements.txt 
- After installing successfully.
- To run:
    - Go to terminal and paste in uvicorn main:app --reload 
    - Wait for it to run a few secs, then this will show up http://127.0.0.1:8000/docs. 
    - Copy and paste the link on to your browsers, you just click the link (don't worry the link is safe!!). 

To do
1. Block Structure [10 points] - DONE
    ○ Define a clear and robust block structure. Each block must contain at least:
        ■ A unique identifier (e.g., block index/height).
        ■ A timestamp (indicating when the block was created/validated).
        ■ Data payload (e.g., a list of transactions, or other forms of data).
        ■ The hash of the previous block (to ensure chain linkage).
        ■ Its own cryptographic hash (calculated from all critical block contents, including the
        previous block's hash).
        ■ Fields relevant to your chosen consensus mechanism (e.g., nonce for PoW, validator
        signature for PoA).
        
2. Cryptographic Hashing & Chain Integrity [10 points] - DONE
    ○ Blocks must be securely linked using cryptographic hashes. The hash of each block must
    depend on the hash of the previous block.
    ○ Implement functionality to calculate and verify block hashes.
    ○ Demonstrate immutability: Show (either programmatically or through clear explanation and
    testing steps in your report) that if data in a previous block is tampered with, it invalidates
    the hash of that block and all subsequent blocks in the chain.

3. Transaction Handling (or Data Management) [6 points] - DONE
    ○ Implement a mechanism to create and include transactions (or generic data entries) within
    blocks.
    ○ Transactions should be part of the data that is hashed to form the block's hash (e.g., by
    including a Merkle root of transactions, or hashing a serialized list of transactions).
    ○ Maintain a pool of pending transactions if your consensus mechanism involves selecting
    transactions for a new block (e.g., miners selecting from a mempool).

4. Consensus Mechanism [6 points]
    ○ Choose, implement, and justify a consensus mechanism to govern how new blocks are
    created, validated, and added to the chain. Options include (but are not limited to):
    ■ Proof-of-Work (PoW): Must include a mining process, a nonce, a difficulty target, and a
    mechanism for difficulty adjustment (even if simplified).
    ■ Proof-of-Stake (PoS) (Simplified): Must include a way to simulate stake, a mechanism for
    validator selection based on stake (can be simplified), and block validation by chosen
    stakers.
    ■ Proof-of-Authority (PoA) (Simplified): Must include a predefined set of authorized
    signers/validators and a mechanism for them to propose and validate blocks.
    ■ Other recognized or justified consensus algorithms.
    ○ The process of achieving consensus (e.g., finding a nonce in PoW) must be clearly
    demonstrable.

5. Double-Spend Prevention [6 points] - DONE
    ○ Implement and clearly demonstrate a mechanism to prevent the same digital asset (even if
    simulated as simple balances or unique transaction IDs) from being spent more than once.
    ○ This could involve:
        ■ Checking transaction history for conflicting spends.
        ■ Implementing a UTXO (Unspent Transaction Output) model.
        ■ Other valid approaches appropriate to your blockchain design.
    ○ You must describe in your report how a user would attempt a double spend and how your
    system prevents it.

6. Global Ordering of Blocks [6 points]
    ○ The blockchain must maintain a clear, chronologically consistent global ordering of blocks,
    primarily enforced by timestamps and the chain structure.
    ○ The consensus mechanism should ensure that valid blocks are added in an orderly fashion.

7. Data Persistence [3 points] - DONE
    ○ The blockchain (the chain of blocks and any relevant state like account balances or UTXO sets)
    must be persistable to storage (e.g., file(s) on disk, a simple database).
    ○ The system should be able to reload the blockchain state from persistent storage upon
    restarting.
     
8. Basic User Interface [3 points] - DONE
    ○ Provide a simple way for a user to interact with your blockchain. This could be:
        ■ A command-line interface (CLI)
        ■ A web interface
    ○ Functionality should include, as appropriate for your design:
    ■ Creating and submitting new transactions/data.
    ■ Initiating the block creation/mining/validation process.
    ■ Viewing the contents of blocks and the overall chain.
    ■ Checking balances or querying data (if applicable).