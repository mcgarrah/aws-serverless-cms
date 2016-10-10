"""
# security.py
# Author: Miguel Saavedra
# Date: 05/08/2016
# Edited: 10/09/2016 | Christopher Treadgold
"""

import datetime
import uuid

import boto3
import botocore

class Security(object):
    """ Provides a function for authentication and authorization of requests
    through a provided token.
    """

    @staticmethod
    def authenticate_and_authorize(token, request, token_table, user_table,
                                   role_table):
        """ Authenticates a token and checks that the associated user has the
        rights to be making a provided request.
        """
        # Get a dynamodb client object from boto3
        try:
            dynamodb = boto3.client('dynamodb')
        except botocore.exceptions.ClientError as e:
            action = "Getting dynamodb client"
            return {"error": e.response["Error"]["Code"],
                    "data": {"exception": str(e), "action": action}}
        
        # Fetch token information from the token table
        try:
            token_info = dynamodb.get_item(TableName=token_table,
                                            Key={"Token": {"S": token}})
        except botocore.exceptions.ClientError as e:
            action = "Fetching token from the token table for authentication"
            return {"error": e.response["Error"]["Code"],
                    "data": {"exception": str(e), "action": action}}
        
        # Check that the token has an entry in the database associated with it
        if not "Item" in token_info:
            action = "Validating token"
            return {"error": "invalidToken",
                    "data": {"token": token, "action": action}}
        
        token_info = token_info["Item"]
        
        # Checks if request is logoutUser as permission is not required
        if request == "logoutUser":
            return True
        
        # Checks that the token has an expiration date
        if not "Expiration" in token_info:
            action = "Validating token"
            return {"error": "invalidTokenNoExpiration",
                    "data": {"token": token, "action": action}}
                    
        token_expiration = token_info["Expiration"]["S"]
        
        # Check that the token is not expired
        if not token_expiration == "None":
            expiration = datetime.datetime.strptime(token_expiration,
                                                    "%a, %d-%b-%Y %H:%M:%S UTC")
            if expiration < datetime.datetime.utcnow():
                action = "Validating token"
                return {"error": "expiredToken",
                        "data": {"token": token, "action": action}}
            
        # Check that the token has a user associated with it
        try:
            user_email = token_info["UserEmail"]["S"]
        except KeyError:
            action = "Fetching user from the user table for authorization"
            return {"error": "tokenHasNoUser",
                    "data": {"token": token, "action": action}}
        
        # Query the user table for the user id extracted from the token table
        try:
            user_info = dynamodb.get_item(
                TableName=user_table,
                Key={"Email": {"S": user_email}}
            )
        except botocore.exceptions.ClientError as e:
            action = "Querying the user table for authorization"
            return {"error": e.response["Error"]["Code"],
                    "data": {"exception": str(e), "action": action}}
        
        # Check that the user id has an enty in the database associated with it
        if not "Item" in user_info:
            action = "Fetching user from the user table for authorization"
            return {"error": "invalidUserAssociatedWithToken",
                    "data": {"user": user_email, "action": action}}
        
        user_info = user_info["Item"]
        
        # Check that the user has a role associated with it
        if not "Role" in user_info:
            action = "Fetching user from the user table for authorization"
            return {"error": "userHasNoRole",
                    "data": {"user": user_email, "action": action}}
        
        user_role = user_info["Role"]["S"]
        
        # Query the role table for the role extracted from the user
        try:
            role_info = dynamodb.get_item(
                TableName=role_table,
                Key={"RoleName": {"S": user_role}}
            )
        except botocore.exceptions.ClientError as e:
            action = "Querying the role table for authorization"
            return {"error": e.response["Error"]["Code"],
                    "data": {"exception": str(e), "action": action}}
        
        # Check that the role name has a role associated with it
        if not "Item" in role_info:
            action = "Fetching role from the role table for authorization"
            return {"error": "invalidRoleAssociatedWithUser",
                    "data": {"user": user_email, "action": action}}
                    
        role_info = role_info["Item"]
                    
        # Check that the role has permissions
        if not "Permissions" in role_info:
            action = "Fetching role from the role table for authorization"
            return {"error": "roleHasNoPermissions",
                    "data": {"user": user_email, "action": action}}
        
        role_permissions = role_info["Permissions"]["SS"]
        
        # Check that the user is authorized to perform the request
        if request in role_permissions or "all" in role_permissions:
            user_info["Permissions"] = role_permissions
            return user_info
        
        # Return error as user did not pass permissions check
        return {"error": "notAuthorizedForRequest",
                "data": {"user": user_email, "request": request}}