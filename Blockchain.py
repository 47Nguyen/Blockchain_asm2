import datetime
import hashlib
import json

class Block:
    def __init__(self, block_index, time_created, transactions, previous_hash, nonce):
        """_summary_

        Args:
            block_index (_type_): _description_
            time_created (_type_): _description_
            transactions (_type_): _description_
            previous_hash (_type_): _description_
            nonce (_type_): _description_
        """
        self.block_index = block_index
        self.time_created = time_created 
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.hash_block()
        self.nonce = nonce

    def to_dict(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "proof": self.proof,
            "previous_hash": self.previous_hash,
        }
    

class Transactions:
    def __init__(self, transaction_id, sender, receiver, amount):
        """_summary_

        Args:
            transaction_id (_type_): _description_
            sender (_type_): _description_
            receiver (_type_): _description_
            amount (_type_): _description_
        """
        self.ids = transaction_id
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
    
    def to_dict(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return {
            "id": self.ids,
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
        }    

class Blockchain: 
    # This class will store data which a normal blockchain should have
    def __init__(self):

        self.chain = []
        self.pending_transactions = []
        self.difficulty =3 
        
        # Populate the block
        genesis_txs = [
            {"id": "tx000", "sender": "ADMIN", "receiver": "Alice", "amount": 1000},
            {"id": "tx0001", "sender": "ADMIN", "receiver": "Jeff", "amount": 1000},
            {"id": "tx0002", "sender": "ADMIN", "receiver": "Carl", "amount": 1000},
            {"id": "tx0003", "sender": "ADMIN", "receiver": "Edward", "amount": 1000},
            {"id": "tx0004", "sender": "ADMIN", "receiver": "Kate", "amount": 1000},
            {"id": "tx0005", "sender": "ADMIN", "receiver": "Joe", "amount": 1000},
            {"id": "tx0006", "sender": "ADMIN", "receiver": "John", "amount": 1000},
        ]
        self.create_block(
            data="Genesis Block",
            proof=1,
            previous_hash="0",
            index=0,
        )
        # Store genesis transactions inside the first block
        self.chain[0]["transactions"] = genesis_txs

    def to_digest(self, new_proof: int, previous_proof: int, index: str, data: str) -> bytes:
        """_summary_

        Args:
            new_proof (int): _description_
            previous_proof (int): _description_
            index (str): _description_
            data (str): _description_

        Returns:
            bytes: _description_
        """
        to_digest = str(new_proof ** 2 - previous_proof **2 + index) + data
        return to_digest.encode()
    
    # Proof of work
    def proof_of_work(self, previous_proof: int, index: int, data: str) -> int:
        """_summary_

        Args:
            previous_proof (int): _description_
            index (int): _description_
            data (str): _description_

        Returns:
            int: _description_
        """
        new_proof = 1
        check_proof = False

        while not check_proof:
            to_digest = self.to_digest(new_proof, previous_proof, index, data)
            hash_value = hashlib.sha256(to_digest).hexdigest()
            if hash_value[:self.difficulty] == "0" * self.difficulty:
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def difficulty_adjustment(self):

        if len(self.chain) %  5 ==0:
            self.difficulty += 1
        elif self.difficulty > 1 and len(self.chain) & 7 == 0:
            self.difficulty -= 1
    
    # Hash value
    def hash_value(self, block):
        """_summary_

        Args:
            block (_type_): _description_

        Returns:
            _type_: _description_
        """
        block_copy = dict(block)
        block_copy.pop("hash", None)

        encoded_block = json.dumps(block_copy, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
              
    # ---- Block ----
    def mine_block(self, data: str, miner: str) -> dict: 
        """_summary_

        Args:
            data (str): _description_
            miner (str): _description_

        Returns:
            dict: _description_
            
        In a real mining situation the attempts can take up to thousands and millions of attempts.
        However, it is probabillistic and can vary. 
        """
        
        #1. Get previous block
        previous_block = self.get_previous_block()
        previous_proof = previous_block["proof"]
        index = previous_block["index"] + 1
        
        # 2. Find valid proof
        proof = self.proof_of_work(previous_proof, index, data)
        
        # 3. When proof is found reward user 
        reward_tx = {
            "id": f"reward_{len(self.chain)+1}",  # unique reward ID
            "sender": "SYSTEM",
            "receiver": miner,
            "amount": 10,  # reward amount
        }
        self.pending_transactions.append(reward_tx)

        # 4, Link preivous hash
        previous_hash = self.hash_value(previous_block)

        # 5.Create the new block with reward + all pending transactions
        block = self.create_block(
            data=data,
            proof=proof,
            previous_hash=previous_hash,
            index=index
        )
        
        # Set difficulty
        self.difficulty_adjustment()
        return block
    
    # Create block
    def create_block(self, data: str, proof: int, previous_hash: str, index: int) -> dict:
        """_summary_

        Args:
            data (str): _description_
            proof (int): _description_
            previous_hash (str): _description_
            index (int): _description_

        Returns:
            dict: _description_
        """
        block = {
            "index": index,
            "timestamp": str(datetime.datetime.now()),
            "data": data,
            "transactions": self.pending_transactions.copy(),   # include txs here
            "proof": proof,
            "previous_hash": previous_hash,
        }
        block["hash"] = self.hash_value(block)
        self.pending_transactions = []  # clear the pool after mining
        self.chain.append(block)
        return block
    
    # Get previous block
    def get_previous_block(self) -> dict:
        """_summary_

        Returns:
            dict: _description_
        """
        return self.chain[-1] 
    
    # Chain integreity 
    def is_chain_valid(self) -> bool: ## Job is to make sure that the chain is still valid and no alteration been made
        """_summary_

        Returns:
            bool: _description_
        """
        previous_block = self.chain[0]
        block_index = 1

        while block_index < len(self.chain):
            block = self.chain[block_index]
            if block['previous_hash'] != self.hash_value(previous_block):
                return False

            current_proof = previous_block['proof']
            next_index, next_data , next_proof = (
                block["index"],
                block["data"],
                block["proof"],
            )
            hash_value = hashlib.sha256(self.to_digest(new_proof=next_proof, previous_proof=current_proof, 
                                                       index = next_index, data = next_data)).hexdigest()
            
            if hash_value[:self.difficulty] != "0" * self.difficulty:
                        return False

            
            previous_block = block
            block_index +=1
        
        return True 
              
    # ---- DATA PERSISTENCE ----
    # Save Blockchain
    def save_chain(self):
        """_summary_
        """
        with open("blockchain.json", "w") as f:
            json.dump(self.chain, f , indent=4)

    # Load block chain
    def load_chain(self):
        """_summary_
        """
        with open("blockchain.json", "r") as f:
             self.chain = json.load(f)

    # ---- TRANSACTIONS ----
    def get_balance(self, user: str) -> float:
        """_summary_

        Args:
            user (str): _description_

        Returns:
            float: _description_
        """
        balance = 0.0

        # Confirmed transactions
        for block in self.chain:
            for tx in block["transactions"]:
                sender = tx.get("sender")
                receiver = tx.get("receiver")
                amount = tx.get("amount", 0)  

                if sender == user:
                    balance -= amount
                if receiver == user:
                    balance += amount

        # Pending transactions
        for tx in self.pending_transactions:
            sender = tx.get("sender")
            receiver = tx.get("receiver")
            amount = tx.get("amount", 0)

            if sender == user:
                balance -= amount
            if receiver == user:
                balance += amount

        return balance

    def check_transactions(self, tx_id: str) -> bool: # Check for duplication transactions_id
        """_summary_

        Args:
            tx_id (str): _description_

        Returns:
            bool: _description_
        """
        if not tx_id:
            return False # No tx exists
        
        for transactions in self.pending_transactions:
            if transactions.get("id") == tx_id:
                return True
        for block in self.chain:
            for transactions in block.get("transactions", []):
                if transactions.get("id") == tx_id:
                    return True
        return False
    
    def exists_transactions(self, tx_id: str) -> bool:
        """_summary_

        Args:
            tx_id (str): _description_

        Returns:
            bool: _description_
        """
        return self.check_transactions(tx_id)

    def insert_transaction(self, transaction: Transactions) -> bool: 
        """_summary_

        Returns:
            _type_: _description_
        """
        if not isinstance(transaction, Transactions):
            return False

        tx = transaction.to_dict()

        if not self.validate_transaction(tx):
            return False

        if self.exists_transactions(tx["id"]):
            return False

        self.pending_transactions.append(tx)

        return True

    def validate_transaction(self, tx: dict) -> bool:
        """_summary_

        Args:
            tx (dict): _description_

        Returns:
            bool: _description_
        """
        sender = tx.get("sender")
        receiver = tx.get("receiver")
        amount = tx.get("amount")

        if not sender or not receiver or amount is None:
            return False

        try:
            amount = float(amount)
        except (TypeError, ValueError):
            return False

        if amount < 0:
            return False

        if sender != "SYSTEM":  # Allow mining rewards or system tx
            balance = self.get_balance(sender)
            if amount > balance:
                return False

        return True