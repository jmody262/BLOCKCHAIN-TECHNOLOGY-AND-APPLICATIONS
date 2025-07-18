import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, proof):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.proof = proof
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{self.proof}"
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.difficulty = 4  # Set difficulty before genesis block
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        print("Creating genesis block...")
        genesis_block = Block(0, "0", str(time.time()), "Genesis Block", 0)
        genesis_block.hash = self.proof_of_work(genesis_block)
        return genesis_block

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = self.proof_of_work(new_block)
        self.chain.append(new_block)

    def proof_of_work(self, block):
        print(f"Mining block {block.index}...")
        proof = 0
        while True:
            block.proof = proof
            hash_attempt = block.calculate_hash()
            if hash_attempt.startswith('0' * self.difficulty):
                return hash_attempt
            proof += 1

    def add_data(self, data):
        index = len(self.chain)
        timestamp = str(time.time())
        previous_hash = self.get_latest_block().hash
        new_block = Block(index, previous_hash, timestamp, data, 0)
        self.add_block(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                print(f"Block {i} has invalid hash!")
                return False

            if current.previous_hash != previous.hash:
                print(f"Block {i} is not linked to Block {i - 1}")
                return False

            if not current.hash.startswith('0' * self.difficulty):
                print(f"Block {i} doesn't meet the difficulty level.")
                return False

        return True


# Example Usage
if __name__ == "__main__":
    blockchain = Blockchain()

    blockchain.add_data("Transaction data for Block 1")
    blockchain.add_data("Transaction data for Block 2")

    print("\nBlockchain validity:", blockchain.is_chain_valid())

    for block in blockchain.chain:
        print(f"\nBlock {block.index}")
        print(f"Timestamp: {block.timestamp}")
        print(f"Data: {block.data}")
        print(f"Proof: {block.proof}")
        print(f"Hash: {block.hash}")
        print(f"Previous Hash: {block.previous_hash}")
