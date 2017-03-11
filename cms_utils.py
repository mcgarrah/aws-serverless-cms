#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
# cms_utils.py
# Author: Gabriel Wu
# Date: N/D
# Edited: 02/24/2017 | Gabriel Wu
"""

import boto3
import botocore
import os
import json
import sys


class CmsUtils:

    def __init__(self, configs):
        self.constants = {}
        for key in configs.keys():
            self.constants[key] = configs[key]

    @staticmethod
    def getAvailableRegions():
        client = boto3.client('ec2')
        regions = [region['RegionName'] for region in
                   client.describe_regions()['Regions']]
        return regions

    def createBucket(self, bucketname, templateBody):
        stackName = bucketname + '-Stack'
        try:
            client = boto3.client('cloudformation')

            response = client.create_stack(StackName=stackName,
                    TemplateBody=templateBody)
            print 'stack created'
            print response

#            waiters = client.waiter_names
#            print waiters

            waiter = client.get_waiter('stack_create_complete')
            waiter.wait(StackName=stackName)

            response = client.describe_stacks(StackName=stackName)
            print 'describe stack'
            print response
        except botocore.exceptions.ClientError, e:

            print e
            sys.exit()

    def uploadFolder(self, bucketname, fileDir):
        print bucketname, fileDir
        bucket = boto3.resource('s3').Bucket(bucketname)
        files = []

        for (dirpath, dirnames, filenames) in os.walk(fileDir):
            for file in filenames:
                files.append(os.path.join(dirpath, file))

#        print files

        for file in files:
            with open(file, 'r') as data:
                key = file[len(file) - len(fileDir):len(file)]
                print file, key

                bucket.put_object(ACL='public-read', Body=data,
                                  StorageClass='STANDARD', Key=key)

    def uploadWebsite(self, prefix):
        self.uploadFolder(self.constants['static_website_bucket'],
                          prefix)


#    def uploadCfnTemplate(self, prefix):
#        self.uploadFolder(self.constants['template_bucket'], prefix)
#
#    def uploadLambda(self, prefix):
#        self.uploadFolder(self.constants['lambda_bucket'], prefix)

