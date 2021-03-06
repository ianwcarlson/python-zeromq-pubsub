schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "id": "http://jsonschema.net",
  "type": "object",
  "properties": {
    "endPointsIds": {
      "id": "http://jsonschema.net/endPointsIds",
      "type": "array",
      "items": {
        "id": "http://jsonschema.net/endPointsIds/2",
        "type": "object",
        "properties": {
          "id": {
            "id": "http://jsonschema.net/endPointsIds/2/id",
            "type": "string"
          },
          "address": {
            "id": "http://jsonschema.net/endPointsIds/2/address",
            "type": "string"
          }
        },
        "required": [
          "id",
          "address"
        ]
      },
      "required": [
        "2"
      ]
    },
    "processList": {
      "id": "http://jsonschema.net/processList",
      "type": "array",
      "items": {
        "id": "http://jsonschema.net/processList/2",
        "type": "object",
        "properties": {
          "processName": {
            "id": "http://jsonschema.net/processList/2/processName",
            "type": "string"
          },
          "processPath": {
            "id": "http://jsonschema.net/processList/2/processPath",
            "type": "string"
          },
          "endPoint": {
            "id": "http://jsonschema.net/processList/2/endPoint",
            "type": "string"
          },
          "subscriptions": {
            "id": "http://jsonschema.net/processList/2/subscriptions",
            "type": "array",
            "items": {
              "id": "http://jsonschema.net/processList/2/subscriptions/0",
              "type": "object",
              "properties": {
                "endPoint": {
                  "id": "http://jsonschema.net/processList/2/subscriptions/0/endPoint",
                  "type": "string"
                },
                "topics": {
                  "id": "http://jsonschema.net/processList/2/subscriptions/0/topics",
                  "type": "array",
                  "items": {
                    "id": "http://jsonschema.net/processList/2/subscriptions/0/topics/1",
                    "type": "string"
                  }
                }
              },
              "additionalProperties": False,
              "required": ["endPoint", "topics"]
            }
          }
        },
        "additionalProperties": False,
        "required": ["processName", "processPath", "endPoint"]
      },
      "additionalItems" : False
    }
  },
  "required": [
    "endPointsIds",
    "processList"
  ]
}