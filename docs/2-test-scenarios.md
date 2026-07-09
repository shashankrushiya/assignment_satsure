# Top 10 Test Scenarios

Ordered from highest to lowest risk.

| ID | Rank | Scenario | Risk | Rationale |
| --- | --- | --- | --- | --- |
| S1 | 1 | Reject invalid submissions instead of persisting bad data | Critical | If invalid input is accepted, the backend contract is broken and the form can silently store unusable responses. |
| S2 | 2 | Persist each submission independently without cross-test contamination | Critical | Shared state would make results non-deterministic and hide real defects in both UI and API coverage. |
| S3 | 3 | Store local timestamps and the correct locale | High | A timezone or locale mismatch would make the captured response incorrect for the target user environment. |
| S4 | 4 | Prefix filtering works by default | High | This is the primary user journey and the default behavior described by FR-02. |
| S5 | 5 | Match-anywhere filtering works when configured | High | The configurable backend mode is a second supported behavior and must not regress. |
| S6 | 6 | Successful submission shows success state and persists the payload | High | The form must complete the REST flow and give the user feedback on success. |
| S7 | 7 | Clicking a suggestion populates the input exactly | Medium | Incorrect selection behavior causes downstream submission failures and user confusion. |
| S8 | 8 | Keyboard interaction works for Enter and Escape | Medium | Keyboard support affects accessibility and common user flow, but it is less critical than data integrity. |
| S9 | 9 | Tab order moves through the form elements predictably | Medium | Focus order is important for usability, but failures here are usually recoverable. |
| S10 | 10 | API rejects malformed requests and unknown ids cleanly | Low | These are negative cases and useful for hardening, but they are less likely to affect the core happy path. |
