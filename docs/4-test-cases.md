# Detailed Test Cases

The test cases below trace back to the ranked scenarios in `docs/2-test-scenarios.md`.

## TC-UI-01

- Title: Tab navigation reaches the input and button in order
- Scenario coverage: S9
- Preconditions: Mock SUT is running; browser opened to the autocomplete form.
- Test steps:
  1. Load the form.
  2. Press Tab once.
  3. Press Tab again.
- Expected results:
  1. Focus lands on `#input-field`.
  2. Focus then moves to `#next-button`.
- Test data: No typed input required.

## TC-UI-02

- Title: Enter submits a valid suggestion selection
- Scenario coverage: S6, S8
- Preconditions: Mock SUT is running in default prefix mode.
- Test steps:
  1. Open the form.
  2. Click the suggestion `agile methodology`.
  3. Press Enter.
- Expected results:
  1. The form submits.
  2. The success container becomes visible.
  3. The error message remains hidden.
- Test data: `agile methodology`

## TC-UI-03

- Title: Escape clears the input and restores the full list
- Scenario coverage: S8
- Preconditions: Mock SUT is running.
- Test steps:
  1. Open the form.
  2. Type `agile method` into the input.
  3. Press Escape.
- Expected results:
  1. The input becomes empty.
  2. The suggestion list returns to all three default items.
- Test data: `agile method`

## TC-UI-04

- Title: Prefix filtering hides non-matching suggestions
- Scenario coverage: S4
- Preconditions: Mock SUT is running in default prefix mode.
- Test steps:
  1. Open the form.
  2. Type `agile methodology p`.
- Expected results:
  1. Only prefix-matching suggestions remain visible.
  2. The visible list contains `agile methodology process` and `agile methodology process testing`.
- Test data: `agile methodology p`

## TC-UI-05

- Title: Match-anywhere filtering keeps substring matches visible
- Scenario coverage: S5
- Preconditions: Mock SUT is running with match-anywhere mode enabled for the form request.
- Test steps:
  1. Open the form in anywhere mode.
  2. Type `process`.
- Expected results:
  1. The two suggestions containing `process` remain visible.
  2. The first suggestion remains hidden because it does not contain the substring.
- Test data: `process`

## TC-UI-06

- Title: Clicking a suggestion populates the input
- Scenario coverage: S7
- Preconditions: Mock SUT is running.
- Test steps:
  1. Open the form.
  2. Click `agile methodology process`.
- Expected results:
  1. The input value becomes `agile methodology process`.
  2. The selection is ready for submission.
- Test data: `agile methodology process`

## TC-API-01

- Title: Valid POST persists and GET returns the exact FR-05 payload
- Scenario coverage: S1, S3, S6
- Preconditions: Backend is running; a unique submission id is available.
- Test steps:
  1. POST a fully valid response body.
  2. GET the stored response by submission id.
- Expected results:
  1. POST returns HTTP 200.
  2. GET returns the same payload.
  3. All required fields are present and correctly typed.
- Test data: `agile methodology`

## TC-API-02

- Title: Schema and type validation reject malformed payloads
- Scenario coverage: S1, S10
- Preconditions: Backend is running.
- Test steps:
  1. POST a body missing one required field.
  2. POST a body with `completed` as a string instead of a boolean.
- Expected results:
  1. Both requests return HTTP 400.
  2. No response is stored for the rejected payloads.
- Test data: Missing `suggestion_list`; `completed="true"`

## TC-API-03

- Title: Unknown submission ids return 404
- Scenario coverage: S10
- Preconditions: Backend is running.
- Test steps:
  1. GET a response using a random submission id that was never posted.
- Expected results:
  1. The server returns HTTP 404.
- Test data: Random UUID

## TC-API-04

- Title: Locale and timestamp rules are enforced on write
- Scenario coverage: S3, S10
- Preconditions: Backend is running.
- Test steps:
  1. POST a payload with locale `en`.
  2. POST a payload with a UTC timestamp ending in `Z`.
- Expected results:
  1. Both requests are rejected.
  2. The backend stores only local-time, `en-IN`-aligned payloads.
- Test data: `en`; `2024-03-15T10:30:00Z`

