from fastapi import Request
from fastapi.responses import JSONResponse


class PinCodeNotFoundError(Exception): 
    def __init__(self, pincode: str):
        self.pincode = pincode
        self.reason =  f"Pincode {self.pincode}does not exist in database. If you think this is an app error, contact the developers"

class InvalidPinCodeError(Exception): 
    def __init__(self, pincode: str):
        self.pincode = pincode
        self.reason = f"Pincode {self.pincode} is in Invalid Format. Please check your pincode again. If you think this is an app error, contact the developers"

# Custom Exception Handlers
async def pincode_not_found_handler(request: Request, exec: PinCodeNotFoundError):
    return JSONResponse(
        status_code=404, 
        content={
            "error": "pincode_not_found", 
            "message": exec.reason,
            "pincode": exec.pincode
        }
    ) 

async def invalid_pincode_handler(request: Request, exec: InvalidPinCodeError): 
    return JSONResponse(
        status_code=404, 
        content={
            "error": "invalid_pincode_error", 
            "message": exec.reason,
            "pincode": exec.pincode
        }
    )

