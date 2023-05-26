#!/bin/bash

set -x

aws s3 sync ./templates/ s3://mysh-cf-templates/
