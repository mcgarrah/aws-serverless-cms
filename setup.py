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
import yaml

regions = cms_utils.CmsUtils.getAvailableRegions()

for region in regions:
    print region

selectedRegion = ''
while not selectedRegion.strip():
    selectedRegion = raw_input('select a region to deploy cms: ')
    if selectedRegion.strip():
        print 'region is ', selectedRegion
        break

cms_name = ''
while not cms_name.strip():
    cms_name = raw_input('input name of your cms: ')
    if cms_name.strip():
        print 'cms name is ', cms_name
        break

if selectedRegion not in regions:
    print selectedRegion, \
        ' is not available, choose default region us-east-1'
    selectedRegion = 'us-east-1'

template_bucket = ''
while not template_bucket.strip():
    template_bucket = \
        raw_input('input name of your cfn template bucket: ')
    if template_bucket.strip():
        print 'cfn template bucket is ', template_bucket
        break

# TODO pass the static_website_bucket to cloudformation

static_website_bucket = ''
while not static_website_bucket.strip():
    static_website_bucket = \
        raw_input('input name of your static website bucket: ')
    if static_website_bucket.strip():
        print 'static website bucket is ', static_website_bucket
        break

result = {}
result['selectedRegion'] = selectedRegion
result['cms_name'] = cms_name
result['template_bucket'] = template_bucket
result['static_website_bucket'] = static_website_bucket

with open('data.yml', 'w') as outfile:
    yaml.dump(result, outfile, default_flow_style=False)

os.system('pause')

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
