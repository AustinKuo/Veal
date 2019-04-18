#!/usr/bin/python 23.6
# -*- coding: utf-8 -*-

import csv
import re

def stream_to_list(obj_body):
    result = []

    lines = obj_body.read().decode("UTF8").splitlines(True)
    data = csv.reader(lines, skipinitialspace=True)
    for row in data:
        result.append(row)

    return result

def list_to_string(csv_data):
    row_data = []

    for row in csv_data:
        # Put '"' to data if there are ',' in data
        new_row = []
        for data in row:
            new_data = str(data)
            if re.compile(',').search(new_data):
                new_data = "\"{0}\"".format(new_data)
            new_row.append(new_data)

        joined_row = ','.join(new_row)
        row_data.append(joined_row)

    raw_data = '\r\n'.join(row_data)

    return raw_data

