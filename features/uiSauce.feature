Feature: SauceDemo Login

  Scenario: Login to SauceDemo with valid parameters
    Given I am on SauceDemo LoginPage
    When I enter username "standard_user" and password "secret_sauce"
     And I click on login button
    Then I should be successfully login to the Inventory page



