#!/bin/bash

source utils/bucket_create.sh && pytest -vv --ds=delight.settings test/
