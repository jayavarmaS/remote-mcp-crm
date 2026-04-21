from fastapi import FastAPI
from routes.auth import router as auth_router
from routes.customer import router as customer_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(customer_router)

@app.get("/")
def root():
    return {"message": "CRM Backend Running 🚀"}