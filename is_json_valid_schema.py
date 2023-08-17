#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# https://stackoverflow.com/questions/7341537/tool-to-generate-json-schema-from-json-data
# https://easy-json-schema.github.io/
import jsonschema
import json
import sys
from typing import *

"""
/content/drive/MyDrive/a.json
{
  "array": [
    1,
    2,
    3
  ],
  "boolean": true,
  "color": "gold",
  "null": null,
  "number": 123,
  "object": {
    "a": "b",
    "c": "d"
  },
  "string": "Hello World"
}

a.schema
{
  "type": "object",
  "required": [],
  "properties": {
    "array": {
      "type": "array",
      "items": {
        "type": "number"
      }
    },
    "boolean": {
      "type": "boolean"
    },
    "color": {
      "type": "string"
    },
    "null": {
      "type": "string"
    },
    "number": {
      "type": "number"
    },
    "object": {
      "type": "object",
      "required": [],
      "properties": {
        "a": {
          "type": "string"
        },
        "c": {
          "type": "string"
        }
      }
    },
    "string": {
      "type": "string"
    }
  }
}
"""
def load_json(json_file:str, schema_file = None)->dict:
  """
  load_json loads a json file and returns a dict
  optionally compares and validates json against a schema file if provided

  @param: json_file: path to json_file
  @param: schema_file: path to schema file to validate against

  @rtype: dict
  @return: returns a dict if json matches the schema
  """
  dd = {}
  if json_file and schema_file:
    if not is_valid_json_for_schema(schema_file, json_file):
      return None

  with open(json_file) as f:
    dd = json.load(f)
    return dd

def save_json(dd_json:Dict, json_file:str, schema_file = None)-> bool:
  """
  save_json saves a json file after optionally comparing it to a schema
  file if provided

  @param: dd_json, a dictionary to save to json 
  @param: json_file: path to json_file
  @param: schema_file: path to schema file to validate against
  @rtype: bool 
  @return :returns False if json does not match the schema
  """
  dd = {}
  if json_file and schema_file:
    if not is_valid_json_for_schema(schema_file, json_file):
      return False
  #
  json_obj = json.dumps(dd_json, indent = 2)
  with open(json_file, "w") as f:
    f.write(json_obj)
  
  return True


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

#main : driver code to run and test lib
json_file = "a.json"
schema_file = None
# argc = len(sys.argv)
# if argc != 3:
#     print(f"Usage: {sys.argv[0]} <json_file> <schema_file>")
#     exit(0)
# json_file = sys.argv[1]
# schema_file = sys.argv[2]
print(f"json_file:{json_file} schema_file:{schema_file}")

dd = load_json("/content/drive/MyDrive/a.json")
print(f"dd:{dd}")

dd["color"] = "orange"
save_json(dd, "/content/drive/MyDrive/b.json")
