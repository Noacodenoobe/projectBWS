You are a data extraction specialist. Your task is to extract all tasks from the "Action Items" table in the following Markdown report and convert them to a clean JSON array.
Each object should have: "title" (from the 'Zadanie' column), "assignee" (from 'Kto?'), "due_date" (from 'Kiedy?'), "priority" (from 'Priorytet'). If any value is missing, use null.
Return ONLY a valid JSON array, no extra text.

--- REPORT START ---
{{report_content}}
--- REPORT END ---