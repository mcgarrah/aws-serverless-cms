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
import setupConfig


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
        if self.constants.has_key('TemplateBucket') \
            and self.constants['TemplateBucket'] != None:
            print 'TemplateBucket exists, bucket name = ', \
                self.constants['TemplateBucket']
            return
        stackName = bucketname + '-Stack'
        try:
            client = boto3.client('cloudformation')

            # #TODO check if stack exists then skip otherwise create

            response = client.create_stack(StackName=stackName,
                    TemplateBody=templateBody)
            print 'stack created'

            waiter = client.get_waiter('stack_create_complete')
            waiter.wait(StackName=stackName)

            response = client.describe_stacks(StackName=stackName)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                outputs = response['Stacks'][0]['Outputs']
                for output in outputs:
                    if output['OutputKey'] == 'TemplateBucket':
                        self.constants['TemplateBucket'] = \
                            output['OutputValue']
                        setupConfig.saveConfig(self.constants)
                        print 'TemplateBucket', \
                            self.constants['TemplateBucket']
        except botocore.exceptions.ClientError, e:

            print e
            sys.exit()

    def uploadFolder(
        self,
        bucketname,
        fileDir,
        acl='private',
        ):

        print 'uploading folder ', fileDir, 'to bucket ', bucketname
        s3 = boto3.resource('s3')
        files = []

        for (dirpath, dirnames, filenames) in os.walk(fileDir):
            for file in filenames:
                files.append(os.path.join(dirpath, file))

#        print files

        for file in files:
            with open(file, 'r') as data:
                key = file[len(fileDir):len(file)]
                print file, key
                s3.meta.client.upload_file(file, bucketname, key)
        print fileDir, 'upload completed'


