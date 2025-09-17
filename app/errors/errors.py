from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


# ✅ Handler para ValueError → 400
async def value_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )


# ✅ Handler para KeyError → 404
async def key_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=404,
        content={"message": str(exc)},
    )


# ✅ Handler para PermissionError → 403
async def permission_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=403,
        content={"message": str(exc)},
    )


# ✅ Handler para RuntimeError → 500
async def runtime_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error", "error": str(exc)},
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ValueError, value_error_handler)
    app.add_exception_handler(KeyError, key_error_handler)
    app.add_exception_handler(PermissionError, permission_error_handler)
    app.add_exception_handler(RuntimeError, runtime_error_handler)
