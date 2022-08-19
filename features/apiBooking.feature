Feature: API basic
  Background:
    Given Created "$.token" at "/auth" URI
      """
      {
          "username" : "admin",
          "password" : "password123"
      }
      """

  @api
  Scenario: Get booking ids
    When Request is sent to "/booking" URI
    Then Response is "200"

  @api
  Scenario: Create a new booking in the API
    When POST Request is sent to "/booking" URI
      """
      {
          "firstname" : "Daniel",
          "lastname" : "Zet",
          "totalprice" : 100,
          "depositpaid" : true,
          "bookingdates" : {
              "checkin" : "2022-04-01",
              "checkout" : "2022-04-02"
          },
          "additionalneeds" : "Breakfast"
      }
      """
    Then Response is "200"
     And Field "$.booking.firstname" in response json is equal to "Daniel"
     And Field "$.booking.lastname" in response json is equal to "Zet"
     And Json response is matching the "single_booking_post" json schema from "booking_schema" file

  @api
  Scenario: Verify created booking with Id parameter
    Given Created booking entry in "/booking" URI with "$.bookingid"
      """
      {
          "firstname" : "Daniel",
          "lastname" : "Zet",
          "totalprice" : 100,
          "depositpaid" : true,
          "bookingdates" : {
              "checkin" : "2022-04-01",
              "checkout" : "2022-04-02"
          },
          "additionalneeds" : "Breakfast"
      }
      """
    When Request is sent to "/booking" URI with created id param
    Then Response is "200"
     And Field "$.firstname" in response json is equal to "Daniel"
     And Field "$.lastname" in response json is equal to "Zet"
     And Json response is matching the "single_booking_get" json schema from "booking_schema" file

  @api
  Scenario: Updates a current booking with Id
    Given Created booking entry in "/booking" URI with "$.bookingid"
      """
      {
          "firstname" : "Daniel",
          "lastname" : "Zet",
          "totalprice" : 100,
          "depositpaid" : true,
          "bookingdates" : {
              "checkin" : "2022-04-01",
              "checkout" : "2022-04-02"
          },
          "additionalneeds" : "Breakfast"
      }
      """
    When PUT Request is sent to "/booking" URI with created id param
      """
        {
            "firstname" : "Dawid",
            "lastname" : "Zetek",
            "totalprice" : 200,
            "depositpaid" : false,
            "bookingdates" : {
                "checkin" : "2022-04-03",
                "checkout" : "2022-04-05"
            },
            "additionalneeds" : "Dinner"
        }
        """
    Then Response is "200"
     And Field "$.firstname" in response json is equal to "Dawid"
     And Field "$.lastname" in response json is equal to "Zetek"

  @api
  Scenario: Update a current booking with a partial payload
    Given Created booking entry in "/booking" URI with "$.bookingid"
      """
      {
          "firstname" : "Daniel",
          "lastname" : "Zet",
          "totalprice" : 100,
          "depositpaid" : true,
          "bookingdates" : {
              "checkin" : "2022-04-01",
              "checkout" : "2022-04-02"
          },
          "additionalneeds" : "Breakfast"
      }
      """
    When PATCH Request is sent to "/booking" URI with created id param
      """
        {
            "firstname" : "Dawid",
            "lastname" : "Zetek"
        }
        """
    Then Response is "200"
     And Field "$.firstname" in response json is equal to "Dawid"
     And Field "$.lastname" in response json is equal to "Zetek"
     And Field "$.additionalneeds" in response json is equal to "Breakfast"

  @api
  Scenario: Delete a current booking
    Given Created booking entry in "/booking" URI with "$.bookingid"
      """
      {
          "firstname" : "Daniel",
          "lastname" : "Zet",
          "totalprice" : 100,
          "depositpaid" : true,
          "bookingdates" : {
              "checkin" : "2022-04-01",
              "checkout" : "2022-04-02"
          },
          "additionalneeds" : "Breakfast"
      }
      """
    When DELETE Request is sent to "/booking" URI with created id param
    Then Response is "201"
