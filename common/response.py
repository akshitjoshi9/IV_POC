from fastapi.responses import JSONResponse


def success_response(message: str, payload: dict = None, status_code: int = 200):
    """ Success response for the API """
    return JSONResponse(
        status_code=status_code,
        content={
            "message": message,
            "status_code": status_code,
            "status": True,
            "payload": payload or {}
        }
    )


def error_response(message: str, status_code: int = 400):
    """ Failer response for the API """
    return JSONResponse(
        status_code=status_code,
        content={
            "message": message,
            "status_code": status_code,
            "status": False,
            "payload": {}
        }
    )
