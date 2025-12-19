import random
from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


app = FastAPI()


class Transaction(BaseModel):
    id: int = Field(..., default_factory=lambda: random.randint(1, 1000), json_schema_extra={"readOnly": True})
    description: str = Field(...)
    amount: float = Field(...)


class TransactionList(BaseModel):
    transactions: list[Transaction] = Field(default_factory=list)

    def add(self, expense: Transaction) -> None:
        self.transactions.append(expense)

    def get(self, transaction_id: int) -> Transaction | None:
        for transaction in self.transactions:
            if transaction.id == transaction_id:
                return transaction
        return None

    def remove(self, transaction_id: int) -> bool:
        for i, transaction in enumerate(self.transactions):
            if transaction.id == transaction_id:
                del self.transactions[i]
                return True
        return False


transaction_list = TransactionList()


@app.get("/transactions/")
def get_transactions():
    return JSONResponse(transaction_list.model_dump(), status_code=status.HTTP_200_OK)


@app.post("/transactions/")
def create_transactions(data: Transaction):
    transaction = Transaction(**data.model_dump())
    transaction_list.add(transaction)
    return JSONResponse(transaction.model_dump(), status_code=status.HTTP_201_CREATED)


@app.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: int):
    transaction = transaction_list.get(transaction_id)
    if transaction is None:
        return JSONResponse({'detail': 'Transaction not found'}, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(transaction.model_dump(), status_code=status.HTTP_200_OK)


@app.put("/transactions/{transaction_id}")
def update_transaction(transaction_id: int, data: Transaction):
    transaction = transaction_list.get(transaction_id)
    if transaction is None:
        return JSONResponse({'detail': 'Transaction not found'}, status_code=status.HTTP_404_NOT_FOUND)
    transaction.description = data.description
    transaction.amount = data.amount
    return JSONResponse(transaction.model_dump(), status_code=status.HTTP_200_OK)


@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int):
    is_deleted = transaction_list.remove(transaction_id)
    if not is_deleted:
        return JSONResponse({'detail': 'Transaction not found'}, status_code=status.HTTP_404_NOT_FOUND)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
