#!/usr/bin/env bash

RESULT=$(cat iris.data | grep -o "Iris-[a-z]\+" | uniq -c)
echo "$RESULT"
