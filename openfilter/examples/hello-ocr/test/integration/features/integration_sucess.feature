Feature: Successful OCR Pipeline Execution

  Scenario: Initialize OCR Filter with valid configuration
    Given a valid OCR filter configuration
    When the OCR filter is initialized
    Then it should create a valid filter instance

  Scenario: Run pipeline with video input
    Given a sample video input file exists
    When the pipeline is executed
    Then an OCR output file should be created
    And the OCR output file should not be empty

  Scenario: Run pipeline with Webvis enabled
    Given the pipeline includes Webvis output
    When the pipeline is executed
    Then the Webvis server should start successfully

  Scenario: Run pipeline and generate benchmark
    Given the pipeline is executed with benchmarking enabled
    When the pipeline finishes
    Then a file named "benchmark_results.csv" should exist
    And the file should contain performance metrics

