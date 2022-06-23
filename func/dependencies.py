from ubiclient import CheckoutManager, CheckoutManagerBase, UbiClientForTest, UbiClient
import json
import sys
from os.path import abspath
from os import pardir, environ

"""
Api Managers are defined 
"""

if 'unitest' in sys.modules.keys():
    with open("{}{}".format(pardir(abspath(__file__)), "resp_checkouts.json"), 'r') as json_file:
        json_obj = json.load(json_file)
    checkout_man = CheckoutManager(UbiClientForTest(json_obj))
else:
    checkout_man = CheckoutManager(UbiClient(environ["X-Ubiregi-Auth-Token"]))


def get_checkout_man() -> CheckoutManagerBase:
    """
    Get api dependency
    Returns:
        CheckoutManagerBase: Instance of CheckoutManager
    """
    return checkout_man
