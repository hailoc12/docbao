#################################################################################
# Program: Create API Auth Token                                                #
# Function: create authentication token to request API provided in docbao_api.py#
# Author: hailoc12                                                              #
# Created: 2019-08-15                                                           #
#################################################################################

from docbao_api import encode_auth_token

print("Create new auth token")
user_id = input("Please input user_id: ")
auth_token = encode_auth_token(user_id)
print("New auth token is: ")
print(auth_token)
