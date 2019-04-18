#!/usr/bin/python 23.6
# -*- coding: utf-8 -*-

import json
import urllib.parse
import boto3

import module.veal_convert as vealc

from module.veal_csv import stream_to_list
from module.veal_csv import list_to_string

OUTPUT_BUCKET = "honda-s3-veal-stew-input"
OUTPUT_FOLDER = "output_veal"

print('Loading function')

s3 = boto3.client('s3')

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print("CONTENT TYPE: " + response['ContentType'])
        body = response['Body']
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

    output_key = "{0}/{1}".format(OUTPUT_FOLDER, key.split('/', 1)[1])

    raw_data = stream_to_list(body)

    output_list = vealc.veal_convert(raw_data)

    try:
        output_str = list_to_string(output_list)
        response = s3.put_object(Bucket=OUTPUT_BUCKET, Key=output_key, Body=output_str)
        # print("OUTPUT Expiration: " + response['ETag'])
    except Exception as e:
        print(e)
        print('Error putting object {} to bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(output_key, OUTPUT_BUCKET))
        raise e

    return "Success"
