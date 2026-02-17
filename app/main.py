from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.endpoints.routes import auth_routes, wallet_routes

app = FastAPI(
    title="Production Blackjack Casino API",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

app.include_router(auth_routes.router)
app.include_router(wallet_routes.router)


# Global Error Handler for consistent response format
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "data": None,
            "message": f"Internal Server Error: {str(exc)}",
        },
    )


@app.get("/")
def health_check():
    return {"success": True, "message": "Casino API is online"}
