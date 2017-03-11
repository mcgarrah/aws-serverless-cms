#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import cms_utils
import yaml


def setupConfig():
    config = {}
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

    lambda_bucket = ''
    while not lambda_bucket.strip():
        lambda_bucket = raw_input('input name of your lambda bucket: ')
        if lambda_bucket.strip():
            print 'lambda bucket is ', lambda_bucket
            break

    config['selectedRegion'] = selectedRegion
    config['cms_name'] = cms_name
    config['template_bucket'] = template_bucket
    config['static_website_bucket'] = static_website_bucket
    config['lambda_bucket'] = lambda_bucket

    setup_config_file = 'setup_config_file.yaml'
    with open(setup_config_file, 'w') as outfile:
        yaml.dump(config, outfile, default_flow_style=False)

    return config


