from typing import Any, Optional
from fastapi.responses import JSONResponse

def success_response(data: Any = None, message: str = "Operation completed successfully", status_code: int = 200) -> JSONResponse:
    """Returns a standardized success JSON response."""
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "data": data,
            "message": message
        }
    )

def error_response(message: str, code: str = "HTTP_400", details: Any = None, status_code: int = 400) -> JSONResponse:
    """Returns a standardized error JSON response."""
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error": {
                "code": code,
                "message": message,
                "details": details
            }
        }
    )
