# Architektura systemu

- Moduł ekstrakcji danych z raportów Markdown (Python, prompt/LLM lub parser)
- Moduł integracji z GitHub Projects (API REST/GraphQL)
- Modularny katalog promptów – łatwa zamiana promptu/modelu pod konkretne zadanie
- Konfiguracja preferowanych modeli w `agent_config/settings.json`
- Wszystkie istotne decyzje i zmiany architektury zapisywane w tym pliku