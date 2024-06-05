import requests

def add_transaction(sender, recipient, amount):
    url = 'http://localhost:5000/transactions/new'
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }
    response = requests.post(url, json=transaction)
    print(response.json())

def mine_block():
    url = 'http://localhost:5000/mine'
    response = requests.get(url)
    print(response.json())

def get_chain():
    url = 'http://localhost:5000/chain'
    response = requests.get(url)
    print(response.json())

if __name__ == '__main__':
    while True:
        print("1. Add Transaction")
        print("2. Mine Block")
        print("3. Display Blockchain")
        choice = input("Enter choice: ")
        if choice == '1':
            sender = input("Enter sender: ")
            recipient = input("Enter recipient: ")
            amount = input("Enter amount: ")
            add_transaction(sender, recipient, amount)
        elif choice == '2':
            mine_block()
        elif choice == '3':
            get_chain()
        else:
            print("Invalid choice")
