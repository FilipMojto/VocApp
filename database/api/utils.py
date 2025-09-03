import logging
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

def handle_integrity_error(e: IntegrityError):
    logging.error(e.orig)
    raise HTTPException(
        status_code=400,
        detail="Constraint violation (e.g. duplicate or null field)",
    )