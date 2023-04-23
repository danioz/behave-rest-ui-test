Feature: API BDD
  Background:
    Given Created "$.token" at "/auth" URI
      """
      {
        "username": "admin",
        "password": "password123"
      }
      """

  @wip
  Scenario: Users creates booking and is able to assert created booking
    When User sends a valid POST request to Booking
      | firstname | lastname       | totalprice | depositpaid | checkin    | checkout   | additionalneeds |
      | Arnold    | Schwarzenegger | 999        | true        | 2018-01-01 | 2019-01-01 | Breakfast       |
    Then Response is "200"
     And Created booking should have data
      | firstname | lastname       | totalprice | depositpaid | checkin    | checkout   | additionalneeds |
      | Arnold    | Schwarzenegger | 999        | true        | 2018-01-01 | 2019-01-01 | Breakfast       |
    When User sends a valid GET request to Booking looking for created booking by Id
    Then Booking response should have data
      | firstname | lastname       | totalprice | depositpaid | checkin    | checkout   | additionalneeds |
      | Arnold    | Schwarzenegger | 999        | true        | 2018-01-01 | 2019-01-01 | Breakfast       |