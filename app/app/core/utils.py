
def is_valid_email_domain(email: str) -> bool:
    _, domain = email.split("@")
    if domain != "uanl.edu.mx":
        return False
    return True
