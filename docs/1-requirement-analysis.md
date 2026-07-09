# Requirement Analysis

## Mock-SUT assumption

The real `https://test.com/autocomplete-form` system and backend are not available in this workspace, so this assignment is implemented against a local mock SUT that mirrors the supplied HTML and REST contract. That assumption is intentional and is the basis for making the tests executable.

## Functional requirements

### FR-01: Text input

- The user can type freely into `#input-field`.
- The user can also click a suggestion to populate the input with an exact value.
- The implementation treats a suggestion click as a valid selection; arbitrary free text remains allowed in the UI but is rejected on submission if it does not match a suggestion.

### FR-02: Prefix filtering, default

- When the page is in default mode, the suggestion list shows items whose text starts with the typed value.
- This is the default behavior for both the UI and the mock backend configuration.

### FR-03: Match-anywhere filtering, configurable

- When the page is opened in match-anywhere mode, suggestions remain visible if they contain the typed text anywhere.
- The mock SUT exposes the mode through configuration so the automation can cover both behaviors without changing code.

### FR-04: Form submission

- Clicking `#next-button` or pressing Enter triggers a REST call.
- A valid exact suggestion selection produces HTTP 200 and the success container becomes visible.
- Invalid input leaves the backend unchanged and shows the error message.

### FR-05: Backend data contract

The persisted response must contain exactly these fields:

| Field | Expected shape |
| --- | --- |
| `account_id` | string |
| `account_email` | string |
| `start_date` | local timestamp string with offset |
| `end_date` | local timestamp string with offset |
| `locale` | IETF BCP 47 tag, expected `en-IN` in this environment |
| `text` | string |
| `suggestion_list` | comma-separated string of matching suggestions only |
| `completed` | boolean |

The mock backend validates the contract on write and serves the stored response back on GET.

## HTML structure implications

The supplied structure is preserved exactly at the element level:

```html
<div class="form-container">
  <label for="input-field">Enter a value:</label>
  <input type="text" id="input-field" placeholder="Type here...">
  <ul class="suggestions">
    <li>agile methodology</li>
    <li>agile methodology process</li>
    <li>agile methodology process testing</li>
  </ul>
  <button id="next-button">Next</button>
  <span class="error-message">Error: Invalid input. Please select a valid suggestion.</span>
  <div class="success-container">
    <p>Success! Your response has been recorded.</p>
  </div>
</div>
```

The mock SUT keeps those ids and classes intact so the page object model can interact with stable selectors.

## Environment implications

- Browser: Chrome is the target browser in the assignment, so the automation is written with Playwright Chromium.
- OS: the assignment says Windows 10, but the automation itself simulates the target environment through browser context settings rather than depending on the host OS.
- Language: English is simulated by setting the Playwright locale to `en-IN`.
- Timezone: India/IST is simulated by setting the Playwright timezone to `Asia/Kolkata`.
- Logged-in user: the mock SUT assumes an already-authenticated session for `test123@gmail.com`.

## Assumptions carried into the implementation

- The local mock SUT is the executable target for both UI and API tests.
- Account identity is fixed in the mock environment and is not part of the login flow.
- The response store is isolated per submission id, and test fixtures reset server state between tests.

