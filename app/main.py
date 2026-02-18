from fastapi import FastAPI

from app.endpoints.routes import auth_routes, wallet_routes, blackjack_routes

app = FastAPI(
    title="Production Blackjack Casino API",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

app.include_router(auth_routes.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(wallet_routes.router, prefix="/api/wallet", tags=["Wallet"])
app.include_router(blackjack_routes.router, prefix="/api/blackjack", tags=["Blackjack"])


@app.get("/")
def health_check():
    return {"success": True, "message": "Casino API is online"}
