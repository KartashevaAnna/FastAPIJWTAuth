UNIVERSAL_401 = {
    "401": {
        "description": "Unauthorized (token is missing or expired)",
    }
}


UNIVERSAL_404 = {
    "404": {
        "description": "Not found",
    }
}

UNIVERSAL_500 = {"500": {"description": "Internal server error"}}

DUPLICATE_409 = {"409": {"description": "Database entry already exists"}}

ERROR_RESPONSES = {
    **UNIVERSAL_401,
    **UNIVERSAL_404,
    **UNIVERSAL_500,
}

UNIVERSAL_200 = {"200": {"description": "Success"}}
