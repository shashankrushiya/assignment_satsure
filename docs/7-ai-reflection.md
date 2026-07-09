## Tools Used

- Codex workspace inspection (5.5 Medium)
- Bundled Python runtime for document extraction and syntax checks
- PowerShell file inspection commands

## Usage Areas

- Extracted the assignment text from the provided DOCX so the implementation could follow the full spec, not a summary.
- Checked the local environment for available Python packages before choosing the mock SUT architecture.
- Ran syntax compilation on the written Python files to catch structural issues before verification.

## Modifications Made

1. I changed the initial plan to isolate persisted backend state by submission id and to reset the store between tests. That was necessary because a single shared in-memory record would let one test overwrite another and make the suite flaky.
2. I corrected the README plan so the tested operating system line is based on the actual verification environment rather than an assumed Windows 10 label. That matters because the submission should be honest about what was really validated.
3. I added explicit traceability from the top-10 scenario list to the detailed test cases so a reviewer can see which risk each test case covers.

## AI Limitations

- The first pass missed the test contamination risk in the shared store design.
- The first plan also assumed a host OS label before it was verified, which would have been a misleading statement if left unchanged.

