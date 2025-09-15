#!/bin/bash
# -*- coding:utf-8 -*-

min=$1
max=$2

for n in $(seq $min $max);
do
    expr="$(head -n $n expresiones.txt | tail -n 1)";
   ./rpn_classifier.py "$expr";
   echo;
done
