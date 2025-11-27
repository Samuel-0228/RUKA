from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .auth.routes import router as auth_router
from .farmers.routes import router as farmers_router
from .consumers.routes import router as consumers_router
from .marketplace.routes import router as marketplace_router
from .payments.routes import router as payments_router
from .admin.routes import router as admin_router
from .config import settings

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="EthioAgriHub API", version="1.0.0",
              description="Digital Ag Platform for Ethiopia")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(farmers_router, prefix="/farmers", tags=["farmers"])
app.include_router(consumers_router, prefix="/consumers", tags=["consumers"])
app.include_router(marketplace_router,
                   prefix="/marketplace", tags=["marketplace"])
app.include_router(payments_router, prefix="/payments", tags=["payments"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])


@app.get("/")
def read_root():
    return {"message": "EthioAgriHub Backend - Serving Ethiopian Farmers!"}
