import json
from dataclasses import asdict
from importlib import import_module
from typing import Any, Dict, Optional

import requests
from behave import given, when, then
from hamcrest import *
from jsonpath_rw import parse
from jsonschema import validate

from dataModel.booking_model import BookingDataModel
from features.apiSteps import jsonSchemaFiles


# region Given
@given('Created "{field_path}" at "{uri}" URI')
def step_impl(context, field_path: str, uri: str):
    payload = json.loads(context.text)
    context.response = requests.post(f'{context.api_url}{uri}', data=payload)
    jsonpath_expression = parse(field_path)
    match = jsonpath_expression.find(context.response.json())
    context.token = match[0].value
    context.headers['Cookie'] = f'token={context.token}'


# endregion

# region When
@when('Request is sent to "{uri}" URI')
def step_impl(context, uri: str):
    context.response = requests.get(f'{context.api_url}{uri}')
    context.test_context['GET'] = context.response.json()


@given('Created booking entry in "{uri}" URI with "{bookingid}"')
@when('POST Request is sent to "{uri}" URI')
def step_impl(context, uri: str, bookingid: Optional[str] = None) -> None:
    payload: Dict[str, Any] = json.loads(context.text)
    context.response = requests.post(f'{context.api_url}{uri}', json=payload)
    if bookingid is not None:
        jsonpath_expression = parse(bookingid)
        match = jsonpath_expression.find(context.response.json())
        context.testcase = match[0].value


@when('User sends a valid POST request to Booking')
def step_impl(context):
    booking: BookingDataModel = parse_booking_table(context)
    booking_dict: Dict[str, Any] = asdict(booking)
    payload: str = json.dumps(booking_dict)

    context.response = requests.post(f'{context.api_url}/booking',headers=context.headers, data=payload)

    json_response: Dict[str, Any] = context.response.json()
    response_to_data_model: BookingDataModel = BookingDataModel(**json_response)

    context.test_context["bookingid"]: int = response_to_data_model.bookingid
    context.test_context["booking"]: BookingDataModel = response_to_data_model.booking

    print(context.test_context['booking'])
    print(context.test_context['bookingid'])

@when('Request is sent to "{uri}" URI with created id param')
def step_impl(context, uri: str):
    context.response = requests.get(f'{context.api_url}{uri}/{context.testcase}')


@when('User sends a valid GET request to Booking looking for created booking by Id')
def step_impl(context):
    context.response = requests.get(f'{context.api_url}/booking/{context.test_context["bookingid"]}')


@when('PUT Request is sent to "{uri}" URI with created id param')
def step_impl(context, uri: str):
    payload = json.loads(context.text)
    context.response = requests.put(f'{context.api_url}{uri}/{context.testcase}', headers=context.headers, json=payload)


@when('PATCH Request is sent to "{uri}" URI with created id param')
def step_impl(context, uri: str):
    payload = json.loads(context.text)
    context.response = requests.patch(f'{context.api_url}{uri}/{context.testcase}', headers=context.headers,
                                      json=payload)


@when('DELETE Request is sent to "{uri}" URI with created id param')
def step_impl(context, uri: str):
    context.response = requests.delete(f'{context.api_url}{uri}/{context.testcase}', headers=context.headers)

# endregion

# region Then
@then('Response is "{http_code}"')
def step_impl(context, http_code: int):
    # Assert
    assert_that(context.response.status_code, equal_to(int(http_code)))


@then('Field "{field_path}" in response json is equal to "{value}"')
def step_impl(context, field_path: str, value: str):
    # Arrange
    jsonpath_expression = parse(field_path)
    match = jsonpath_expression.find(context.response.json())

    # Assert
    assert_that(match[0].value, equal_to(value))


@then('Json response is matching the schema')
def step_impl(context):
    # Arrange
    json_schema = json.loads(context.text)

    # Assert
    validate(context.response.json(), json_schema)


@then('Json response is matching the "{json_schema}" json schema from "{schema_file_name}" file')
def step_impl(context, json_schema: str, schema_file_name: str):
    json_schema_file = import_module(f'.{schema_file_name}', jsonSchemaFiles.__name__)
    loaded_schema = json.loads(getattr(json_schema_file, json_schema))
    validate(context.response.json(), loaded_schema)


@then('Created booking should have data')
@then('Booking response should have data')
def step_impl(context):
    # Arrange
    booking: BookingDataModel.Booking = parse_booking_table(context)
    expected_booking: Dict[str, Any] = asdict(booking)

    # Act
    actual_booking: Dict[str, Any] = context.test_context["booking"]

    # Assert
    assert_that(expected_booking, equal_to(actual_booking))

# endregion


def parse_booking_table(context):
    booking = None
    for row in context.table:
        booking_dates = BookingDataModel.BookingDates(checkin=row['checkin'], checkout=row['checkout'])
        booking = BookingDataModel.Booking(
            firstname=row['firstname'],
            lastname=row['lastname'],
            totalprice=int(row['totalprice']),
            depositpaid=bool(row['depositpaid']),
            bookingdates=booking_dates,
            additionalneeds=row['additionalneeds'])

    return booking
