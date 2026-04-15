from fastapi import FastAPI
from routes import auth, customer

app = FastAPI()

app.include_router(auth.router)
app.include_router(customer.router)

@app.get("/")
def root():
    return {"message": "CRM Backend Running 🚀"}