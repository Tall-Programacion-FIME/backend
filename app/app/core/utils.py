def is_valid_email_domain(email: str) -> bool:
    if "@uanl.edu.mx" not in email:
        return False
    return True
