import traceback

from fastapi import Request
from fastapi.responses import JSONResponse


def register_error_handlers(app):
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        print("🔴 ERROR atrapado:", str(exc))
        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "error": str(exc),
                "type": exc.__class__.__name__,
                "path": request.url.path,
            },
        )
