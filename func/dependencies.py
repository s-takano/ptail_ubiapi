from orm import CheckoutManager

"""
For a real application a "real" ORM mapper with a real database connection must be defined here or in the get_db method.
This database connection is for demonstration purposes only.
"""
db = CheckoutManager()


def get_db() -> CheckoutManager:
    """
    Get database dependency
    Returns:
        CheckoutManager: Instance of database manager
    """
    return db
