from ubiclient import CheckoutManager, CheckoutManagerBase, UbiClientForTest
import json

"""
Api Managers are defined 
"""

with open("C:\\Projects\\Ponytail\\ubiclient\\tests\\unit\\resp_checkouts.json", 'r') as json_file:
    json_obj = json.load(json_file)

checkout_man = CheckoutManager(UbiClientForTest(json_obj))


def get_checkout_man() -> CheckoutManagerBase:
    """
    Get api dependency
    Returns:
        CheckoutManagerBase: Instance of CheckoutManager
    """
    return checkout_man
