#!/bin/bash

awslocal s3 mb s3://${AWS_BUCKET_NAME} --region eu-north-1
awslocal s3 put-bucket-acl --bucket ${AWS_BUCKET_NAME} --acl public-read
