#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# https://stackoverflow.com/questions/7341537/tool-to-generate-json-schema-from-json-data
# https://easy-json-schema.github.io/
import jsonschema
import json
import sys

def get_json_from_file(json_file)->dict:
        # Opening JSON file
        f = open(json_file)
        # returns JSON object as a dictionary
        json_data = json.load(f)
        return json_data

def is_valid_json_for_schema(schema_file:str, json_file:str)->bool:
    json_data = get_json_from_file(json_file)
    schema = get_json_from_file(schema_file)
    print(f"Validating {json_file} against schema in {schema_file}")
    # Validate the valid data
    try:
        jsonschema.validate(json_data, schema)
        print(f"VALID: {json_file} is valid according to the schema {schema_file}.")
        return True
    except jsonschema.exceptions.ValidationError as e:
        print(e)
        print(f"INVALID: {json_file} is not valid according to the schema {schema_file}.")
        return False

#main
json_file = "event.json"
argc = len(sys.argv)
if argc != 3:
    print(f"Usage: {sys.argv[0]} <json_file> <schema_file>")
    exit(0)
json_file = sys.argv[1]
schema_file = sys.argv[2]
print(f"json_file:{json_file} schema_file:{schema_file}")

res = is_valid_json_for_schema(schema_file, json_file)
print(f"res:{res}")
