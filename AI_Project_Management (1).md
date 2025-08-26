# Agent zarządzania projektami (jak kierownik w Asanie)

## Co robi?
Wyobraź sobie kierownika, któremu mówisz „zrób projekt” i on od razu tworzy go
w Asanie. Ten agent słucha twoich poleceń na czacie i wykonuje je w Asanie:
dodaje projekty, zadania, a nawet podzadania.

## Jak działa
1. **Piszesz polecenie** – np. „Stwórz projekt Strona WWW”.
2. **Agent Project Manager** rozumie, o co prosisz i wybiera odpowiednią akcję w
   Asanie.
3. **Simple Memory** zapamiętuje rozmowę, więc agent pamięta, nad czym
   pracujecie.
4. **Think** pomaga mu lepiej zrozumieć złożone instrukcje.

## Jak uruchomić
1. W n8n kliknij **Import** i wybierz plik `AI Project Management.json`.
2. W zakładce **Credentials** dodaj klucz API do Asany.
3. Węzeł z modelem LLM ustaw na lokalny, zgodnie z poradnikiem
   [Local_LLM_Setup.md](Local_LLM_Setup.md) (np. `llama3-8b`).
4. Kliknij **Execute Workflow** i wpisuj polecenia w okienku czatu n8n.

## Przykład użycia
```
Ty: "Dodaj zadanie 'Naprawić bugi' do projektu 'Strona WWW'"
Agent: "Gotowe, zadanie dodane!"
```

