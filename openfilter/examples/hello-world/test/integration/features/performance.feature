Feature: Handle pipeline misconfiguration and failures

  Scenario: Initialize OCR Filter with invalid engine
    Given an OCR filter configuration with an invalid engine
    When the OCR filter is initialized
    Then it should raise a ValueError

  Scenario: Execute pipeline with missing video file
    Given a configuration with a non-existent video file path
    When the pipeline is executed
    Then it should raise a FileNotFoundError

  Scenario: Execute pipeline with missing outputs
    Given a pipeline configuration without defined outputs
    When the pipeline is executed
    Then it should log a configuration error and not crash
