# Zasady dla agenta AI

1. Zawsze korzystaj z promptów z katalogu `agent_config/prompts/`.
2. Wyniki działania umieszczaj w katalogu `data/` oraz jako taski w `project/tasks.md`.
3. Do konwersji Action Items do JSON używaj promptu `action_items_to_json.md`.
4. Po każdym nowym zadaniu lub zmianie projektu aktualizuj `project/plan.md` oraz `docs/README.md`.
5. Dobór modelu językowego:
   - Do ekstrakcji danych z tabel: preferuj modele z dobrą rozumieniem struktury (np. Claude, GPT-4, Llama3-70B, Bielik-7B dla polskiego).
   - Do streszczeń, podsumowań i generowania tekstów po polsku: modele finetunowane na polskim (Bielik, Llama3-70B, Command R+).
   - Do kodowania: GPT-4, Claude Opus, Llama3-70B-Code.
6. Każda większa zmiana workflow powinna być odnotowana w `project/architecture.md`.