from fastapi import Depends, HTTPException, status

from app.auth.dependencies import get_current_user


def require_admin(
    current_user=Depends(get_current_user),
):
    """
    Allow only admins.
    """

    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins only.",
        )

    return current_user


def require_user(
    current_user=Depends(get_current_user),
):
    """
    Any authenticated user.
    """

    return current_user