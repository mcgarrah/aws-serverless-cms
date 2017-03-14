#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
# setup.py
# Author: Christopher Treadgold
# Date: N/D
# Edited: 07/08/2016 | Christopher Treadgold
# Edited: 14/03/2017 | Gabriel Wu
"""

import sys
import os
import cms_utils
import yaml
import setupConfig

if len(sys.argv) == 2 and sys.argv[1] == '-loadConfig':
    config = {}
    with open('setup_config_file.yaml', 'r') as data:
        config = yaml.load(data)
else:

    config = setupConfig.setupConfig()

print config
util = cms_utils.CmsUtils(config)

# create bucket for init bucket to store templates

with open('initTemplate/init-template-bucket.yaml', 'r') as \
    templateBody:
    templateBody = templateBody.read()
    util.createBucket(config['template_bucket'], templateBody)

# get top level template and populate it with bucketname

topLevelTemplate = ''
with open('initTemplate/00-top-level-cms.template', 'r') as \
    topLevelTemplate:
    topLevelTemplate = topLevelTemplate.read()
    topLevelTemplate = topLevelTemplate.replace('{s3-bucketname}',
            util.constants['TemplateBucket'])
with open('cfnTemplate/00-top-level-cms.yaml', 'w') as startTemplate:
    startTemplate.write(topLevelTemplate)

# upload templates

util.uploadTemplateFolder(util.constants['TemplateBucket'], '.'
                          + os.sep + 'cfnTemplate' + os.sep)

util.createStackFromS3(util.constants['uploadTemplateFolderDict'
                       ]['00-top-level-cms.yaml'], 'myCmsStack')

# start building with templates

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
