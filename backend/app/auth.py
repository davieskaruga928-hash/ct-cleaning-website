import os
from fastapi import Header, HTTPException, status

# Set this in your .env file. Do NOT commit a real password to git.
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "changeme")


def require_admin(x_admin_password: str = Header(default="")):
    """Simple shared-password check for the admin dashboard.

    Not a full auth system — good enough for one or two people managing
    leads. Revisit if more users or stronger security are ever needed.
    """
    if x_admin_password != ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin password",
        )
