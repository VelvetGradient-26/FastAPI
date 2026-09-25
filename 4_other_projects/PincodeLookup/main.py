from data import PINCODES
from exceptions import *
from fastapi import FastAPI
from models import *

app = FastAPI()

# Register your custom exception handler
app.add_exception_handler(PinCodeNotFoundError, pincode_not_found_handler)
app.add_exception_handler(InvalidPinCodeError, invalid_pincode_handler)

# APP Routes
@app.get("/")
def root(): 
    return {'message': "Hello!"}

@app.get("/pincode/{code}", response_model=LocationResponse)
def lookup_pincode(code: str): 
    if len(code) != 6 or not code.isdigit(): 
        raise InvalidPinCodeError(code)

    if code not in PINCODES: 
        raise PinCodeNotFoundError(code)
    return PINCODES[code]

@app.post("/pincode/bulk", response_model=BulkResponse)
def bulk_lookup(request: BulkPincodeRequest): 
    results = []
    missing = []

    for code in request.pincodes: 
        if code in PINCODES: 
            results.append(PINCODES[code])
        else: 
            missing.append(code)

    return BulkResponse(
        found=len(results), 
        not_found=len(missing), 
        results=results, 
        missing=missing
    )