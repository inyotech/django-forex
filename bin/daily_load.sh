#!/bin/bash

base_path=$(dirname $(readlink -f "$0"))/../

python_interpreter=${base_path}/venv/bin/python

$python_interpreter ${base_path}/forex/manage.py loadrates

$python_interpreter ${base_path}/forex/manage.py loadstories

