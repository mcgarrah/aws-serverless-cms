#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
# setup.py
# Author: Christopher Treadgold
# Date: N/D
# Edited: 07/08/2016 | Christopher Treadgold
"""

import cms_functions
import sys
import os
import cms_utils

regions = cms_utils.CmsUtils.getAvailableRegions()

for region in regions:
    print region

selectedRegion = raw_input('select a region to deploy cms: ')
cms_name = raw_input('input name of your cms: ')

if selectedRegion not in regions:
    print selectedRegion, \
        ' is not available, choose default region us-east-1'
    selectedRegion = 'us-east-1'

print selectedRegion, ' is selected and cms with name = ', cms_name

cms = cms_functions.AwsFunc(cms_name, region=selectedRegion)

# Create tje rest api

# cms.create_rest_api()

## Create the lambda function
# cms.create_lambda_function()
#
## Setup the rest api
# cms.api_add_post_method()
# cms.api_add_options_method()
# cms.deploy_api()
#
## Create the s3 bucket
# cms.create_bucket()
## Create the cloudfront distribution
## cms.create_cloudfront_distribution() TODO: Reactivate
#
## Create the dynamodb blog table
# cms.create_blog_table()
#
## Create the dynamodb page table
# cms.create_page_table()
#
## Create the dynamodb token table
# cms.create_token_table()
#
## Create the dunamodb role table
# cms.create_role_table()
## Add an admin role to the role table
# cms.create_admin_role_db_entry() //todo
#
## Create the dynamodb user table
# cms.create_user_table()
## Add an admin to the user table
# cms.create_admin_user_db_entry() //todo
#
## Print the default login credentials and the login link
# cms.print_login_link()
#
## Saves the cms installation information
# cms.save_constants()
