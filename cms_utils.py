#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
# cms_functions.py
# Author: Gabriel Wu
# Date: N/D
# Edited: 02/24/2017 | Gabriel Wu
"""

import boto3
import botocore


class CmsUtils:

    def __init__(self):
        print self

    @staticmethod
    def getAvailableRegions():
        client = boto3.client('ec2')
        regions = [region['RegionName'] for region in
                   client.describe_regions()['Regions']]
        return regions
    
    def uploadFiles():
        

