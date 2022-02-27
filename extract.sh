#!/bin/bash

find fonts -name "*.zip" -execdir unzip -o {} \;
find fonts -name "*.zip" -exec rm {} \;
