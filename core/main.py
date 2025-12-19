import random
from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse


app = FastAPI()


transactions = dict()


@app.get("/transactions/")
def get_transactions():
    return JSONResponse(transactions, status_code=status.HTTP_200_OK)


@app.post("/transactions/")
def create_transactions(description: str, amount: float):
    id = random.randint(1, 1000)
    new_transaction = {'description': description,'amount': amount}
    transactions[id] = new_transaction
    return JSONResponse({f'id': new_transaction}, status_code=status.HTTP_201_CREATED)


@app.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: int):
    if transaction_id not in transactions.keys():
        return JSONResponse({'detail': 'Transaction not found'}, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(transactions.get(transaction_id), status_code=status.HTTP_200_OK)


@app.put("/transactions/{transaction_id}")
def update_transaction(transaction_id: int, description: str, amount: float):
    if transaction_id not in transactions.keys():
        return JSONResponse({'detail': 'Transaction not found'}, status_code=status.HTTP_404_NOT_FOUND)
    updated_transaction = {'description': description,'amount': amount}
    transactions[transaction_id] = updated_transaction
    return JSONResponse({f'{transaction_id}': updated_transaction}, status_code=status.HTTP_200_OK)


@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int):
    if transaction_id not in transactions.keys():
        return JSONResponse({'detail': 'Transaction not found'}, status_code=status.HTTP_404_NOT_FOUND)
    transactions.pop(transaction_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

