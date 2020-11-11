import json
from jsonschema import validate


def assert_valid_schema(data, schema_file):
    with open(schema_file) as f:
        schema = json.load(f)
    return validate(instance=data, schema=schema)


def test_get_post(api_client_brew):
    res = api_client_brew.get_brew(
        path="/todos/1"
    )
    assert_valid_schema(res.json(), 'schema.json')