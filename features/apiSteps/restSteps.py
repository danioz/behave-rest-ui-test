from behave import given, when, then
import requests
from hamcrest import *
import json
from jsonpath_rw import parse
from importlib import import_module
from features.apiSteps import jsonSchemaFiles
from jsonschema import validate


# region Given
@given('Created "{field_path}" at "{uri}" URI')
def step_impl(context, field_path, uri):
    payload = json.loads(context.text)
    context.response = requests.post(f'{context.api_url}{uri}', data=payload)
    jsonpath_expression = parse(field_path)
    match = jsonpath_expression.find(context.response.json())
    context.token = match[0].value
    context.headers = {
        'Cookie': f'token={context.token}'
    }

# endregion

# region When
@when('Request is sent to "{uri}" URI')
def step_impl(context, uri):
    context.response = requests.get(f'{context.api_url}{uri}')


@given('Created booking entry in "{uri}" URI with "{bookingid}"')
@when('POST Request is sent to "{uri}" URI')
def step_impl(context, uri, bookingid=None):
    payload = json.loads(context.text)
    context.response = requests.post(f'{context.api_url}{uri}', json=payload)
    if bookingid is not None:
        jsonpath_expression = parse(bookingid)
        match = jsonpath_expression.find(context.response.json())
        context.testcase = match[0].value


@when('Request is sent to "{uri}" URI with created id param')
def step_impl(context, uri):
    context.response = requests.get(f'{context.api_url}{uri}/{context.testcase}')


@when('PUT Request is sent to "{uri}" URI with created id param')
def step_impl(context, uri):
    payload = json.loads(context.text)
    context.response = requests.put(f'{context.api_url}{uri}/{context.testcase}', headers=context.headers, json=payload)


@when('PATCH Request is sent to "{uri}" URI with created id param')
def step_impl(context, uri):
    payload = json.loads(context.text)
    context.response = requests.patch(f'{context.api_url}{uri}/{context.testcase}', headers=context.headers,
                                      json=payload)


@when('DELETE Request is sent to "{uri}" URI with created id param')
def step_impl(context, uri):
    context.response = requests.delete(f'{context.api_url}{uri}/{context.testcase}', headers=context.headers)
# endregion

# region Then
@then('Response is "{http_code}"')
def step_impl(context, http_code):
    assert_that(context.response.status_code, equal_to(int(http_code)))


@then('Field "{field_path}" in response json is equal to "{value}"')
def step_impl(context, field_path, value):
    jsonpath_expression = parse(field_path)
    match = jsonpath_expression.find(context.response.json())

    assert_that(match[0].value, equal_to(value))


@then('Json response is matching the schema')
def step_impl(context):
    json_schema = json.loads(context.text)
    validate(context.response.json(), json_schema)


@then('Json response is matching the "{json_schema}" json schema from "{schema_file_name}" file')
def step_impl(context, json_schema, schema_file_name):
    json_schema_file = import_module(f'.{schema_file_name}', jsonSchemaFiles.__name__)
    loaded_schema = json.loads(getattr(json_schema_file, json_schema))
    validate(context.response.json(), loaded_schema)
# endregion
