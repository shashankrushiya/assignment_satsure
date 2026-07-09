from __future__ import annotations

import json
from html import escape

from .config import SUGGESTIONS, Settings


def render_form_html(settings: Settings, filter_mode: str) -> str:
    config = {
        "apiBaseUrl": settings.base_url,
        "accountId": settings.account_id,
        "accountEmail": settings.account_email,
        "locale": settings.locale,
        "timezone": settings.timezone,
        "filterMode": filter_mode,
        "suggestions": list(SUGGESTIONS),
    }

    config_json = json.dumps(config)
    title = escape("Autocomplete Form")

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    :root {{
      color-scheme: light;
      --page-bg: #f4efe8;
      --panel-bg: #ffffff;
      --ink: #1f2937;
      --muted: #6b7280;
      --accent: #2457ff;
      --accent-strong: #1637b7;
      --border: #d1d5db;
      --success-bg: #e8fff0;
      --success-ink: #126b35;
      --error-bg: #fff0f0;
      --error-ink: #a11b1b;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      font-family: "Segoe UI", Arial, sans-serif;
      background:
        radial-gradient(circle at top left, rgba(36, 87, 255, 0.12), transparent 30%),
        radial-gradient(circle at bottom right, rgba(18, 107, 53, 0.08), transparent 22%),
        var(--page-bg);
      color: var(--ink);
      display: grid;
      place-items: center;
      padding: 24px;
    }}
    .form-container {{
      width: min(100%, 720px);
      background: var(--panel-bg);
      border: 1px solid var(--border);
      border-radius: 24px;
      padding: 32px;
      box-shadow: 0 20px 60px rgba(31, 41, 55, 0.08);
    }}
    .form-container h1 {{
      margin: 0 0 20px;
      font-size: 2rem;
      letter-spacing: -0.03em;
    }}
    label {{
      display: block;
      font-weight: 600;
      margin-bottom: 10px;
    }}
    input {{
      width: 100%;
      min-height: 48px;
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 12px 16px;
      font-size: 1rem;
      outline: none;
    }}
    input:focus {{
      border-color: var(--accent);
      box-shadow: 0 0 0 4px rgba(36, 87, 255, 0.12);
    }}
    ul.suggestions {{
      list-style: none;
      margin: 16px 0 0;
      padding: 0;
      border: 1px solid var(--border);
      border-radius: 16px;
      overflow: hidden;
      background: #fff;
    }}
    ul.suggestions li {{
      padding: 14px 16px;
      border-top: 1px solid var(--border);
      cursor: pointer;
      transition: background 120ms ease;
    }}
    ul.suggestions li:first-child {{
      border-top: none;
    }}
    ul.suggestions li:hover,
    ul.suggestions li:focus-visible {{
      background: rgba(36, 87, 255, 0.08);
      outline: none;
    }}
    .actions {{
      display: flex;
      justify-content: flex-end;
      margin-top: 20px;
    }}
    #next-button {{
      border: none;
      border-radius: 14px;
      padding: 12px 22px;
      font-size: 1rem;
      color: white;
      background: linear-gradient(135deg, var(--accent), var(--accent-strong));
      cursor: pointer;
    }}
    #next-button:hover {{
      filter: brightness(1.05);
    }}
    .error-message,
    .success-container {{
      display: none;
      margin-top: 18px;
      padding: 14px 16px;
      border-radius: 14px;
      font-weight: 600;
    }}
    .error-message {{
      background: var(--error-bg);
      color: var(--error-ink);
    }}
    .success-container {{
      background: var(--success-bg);
      color: var(--success-ink);
    }}
    .status-meta {{
      margin-top: 8px;
      color: var(--muted);
      font-size: 0.92rem;
    }}
  </style>
</head>
<body>
  <div class="form-container">
    <h1>Autocomplete Form</h1>
    <label for="input-field">Enter a value:</label>
    <input type="text" id="input-field" placeholder="Type here..." autocomplete="off">
    <div class="status-meta" id="filter-mode-note"></div>
    <ul class="suggestions" aria-label="Suggestions"></ul>
    <div class="actions">
      <button id="next-button" type="button">Next</button>
    </div>
    <span class="error-message">Error: Invalid input. Please select a valid suggestion.</span>
    <div class="success-container">
      <p>Success! Your response has been recorded.</p>
    </div>
  </div>

  <script>
    window.__AUTOCOMPLETE_CONFIG__ = {config_json};
  </script>
  <script>
    (function() {{
      const config = window.__AUTOCOMPLETE_CONFIG__;
      const suggestions = config.suggestions.slice();
      const input = document.getElementById('input-field');
      const list = document.querySelector('ul.suggestions');
      const nextButton = document.getElementById('next-button');
      const errorMessage = document.querySelector('.error-message');
      const successContainer = document.querySelector('.success-container');
      const filterModeNote = document.getElementById('filter-mode-note');
      const pageState = {{
        startDate: null,
        submissionId: null
      }};
      window.__AUTOCOMPLETE_STATE__ = pageState;

      filterModeNote.textContent = 'Suggestion mode: ' + config.filterMode + ' match';

      function pad(value) {{
        return String(value).padStart(2, '0');
      }}

      function formatLocalTimestamp(date) {{
        const offset = -date.getTimezoneOffset();
        const sign = offset >= 0 ? '+' : '-';
        const absolute = Math.abs(offset);
        const hours = pad(Math.floor(absolute / 60));
        const minutes = pad(absolute % 60);
        return [
          date.getFullYear(),
          '-',
          pad(date.getMonth() + 1),
          '-',
          pad(date.getDate()),
          'T',
          pad(date.getHours()),
          ':',
          pad(date.getMinutes()),
          ':',
          pad(date.getSeconds()),
          sign,
          hours,
          ':',
          minutes
        ].join('');
      }}

      function hideMessages() {{
        errorMessage.style.display = 'none';
        successContainer.style.display = 'none';
      }}

      function showError() {{
        successContainer.style.display = 'none';
        errorMessage.style.display = 'block';
      }}

      function showSuccess() {{
        errorMessage.style.display = 'none';
        successContainer.style.display = 'block';
      }}

      function matches(value, suggestion) {{
        const search = value.trim().toLowerCase();
        const target = suggestion.toLowerCase();
        if (!search) {{
          return true;
        }}
        if (config.filterMode === 'anywhere') {{
          return target.includes(search);
        }}
        return target.startsWith(search);
      }}

      function filteredSuggestions() {{
        const value = input.value.trim();
        return suggestions.filter((suggestion) => matches(value, suggestion));
      }}

      function renderSuggestions() {{
        const visibleSuggestions = filteredSuggestions();
        list.innerHTML = '';
        visibleSuggestions.forEach((suggestion) => {{
          const item = document.createElement('li');
          item.textContent = suggestion;
          item.tabIndex = -1;
          item.addEventListener('click', () => {{
            input.value = suggestion;
            hideMessages();
            renderSuggestions();
            input.focus();
          }});
          list.appendChild(item);
        }});
      }}

      function isValidSelection() {{
        return suggestions.includes(input.value.trim());
      }}

      function matchingSuggestionListForValue(value) {{
        const normalized = value.trim().toLowerCase();
        return suggestions.filter((suggestion) => {{
          const target = suggestion.toLowerCase();
          if (!normalized) {{
            return false;
          }}
          if (config.filterMode === 'anywhere') {{
            return target.includes(normalized);
          }}
          return target.startsWith(normalized);
        }});
      }}

      async function submitResponse() {{
        hideMessages();
        if (!isValidSelection()) {{
          showError();
          return;
        }}

        const now = new Date();
        const payload = {{
          account_id: config.accountId,
          account_email: config.accountEmail,
          start_date: pageState.startDate,
          end_date: formatLocalTimestamp(now),
          locale: config.locale,
          text: input.value.trim(),
          suggestion_list: matchingSuggestionListForValue(input.value).join(', '),
          completed: true
        }};

        try {{
          const response = await fetch(config.apiBaseUrl + '/api/responses', {{
            method: 'POST',
            headers: {{
              'Content-Type': 'application/json',
              'X-Submission-Id': pageState.submissionId,
              'X-Filter-Mode': config.filterMode
            }},
            body: JSON.stringify(payload)
          }});

          if (!response.ok) {{
            showError();
            return;
          }}

          showSuccess();
        }} catch (error) {{
          showError();
        }}
      }}

      input.addEventListener('input', () => {{
        hideMessages();
        renderSuggestions();
      }});

      input.addEventListener('keydown', (event) => {{
        if (event.key === 'Enter') {{
          event.preventDefault();
          submitResponse();
          return;
        }}

        if (event.key === 'Escape') {{
          event.preventDefault();
          input.value = '';
          hideMessages();
          renderSuggestions();
        }}
      }});

      nextButton.addEventListener('click', submitResponse);

      pageState.startDate = formatLocalTimestamp(new Date());
      pageState.submissionId = crypto.randomUUID();
      renderSuggestions();
    }})();
  </script>
</body>
</html>
"""
