# Sovereign Intelligence – Repozytorium zarządzania projektami przez AI

Repozytorium służy do automatyzacji zadań projektowych na bazie transkrypcji spotkań, z wykorzystaniem AI (LLM), integracji z GitHub Projects i zaawansowanego workflow.

## Funkcje
- Automatyczna konwersja zadań z raportu Markdown do JSON
- Wysyłka zadań do GitHub Projects (klasyczny lub Beta)
- Modularne prompty do różnych typów analizy (podsumowania, Action Items, ryzyka)
- Łatwe dostosowanie do nowych modeli LLM

## Struktura
- `agent_config/` – konfiguracja agentów, prompty, zasady
- `src/` – kod automatyzujący import i przetwarzanie
- `project/` – plany, architektura, lista zadań
- `docs/` – dokumentacja techniczna i użytkowa

## Jak używać
1. Umieść raport spotkania w `data/sample_report.md`
2. Uruchom `src/markdown_to_json.py` by wygenerować JSON zadań
3. Uruchom `src/github_projects_importer.py` by wysłać zadania do GitHub Projects

## Wskazówki dot. modeli LLM
- **Bielik-7B** – szybka analiza i podsumowania po polsku
- **Llama3-70B** – głębokie wnioskowanie, duże projekty, kodowanie
- **GPT-4/Claude** – najwyższa precyzja, skomplikowane ekstrakcje danych