# Instrukcja projektu na GitHub — „Las (Berlin) – Ops + AI”
**Wersja:** 2025-08-26 01:54  
**Cel:** jedno repo, które porządkuje dokumenty projektu (plan, checklisty, materiały) **i** dodaje automatyczne przepływy z AI do organizacji zadań.

---

## 1) Jak rozumiem Twoją potrzebę
Chcesz mieć **jedno źródło prawdy**: dokumenty + listy + plan + checklisty, a do tego **sprytną automatyzację**:
- szybkie zamienianie notatek/PDF/zdjęć w **zadania**,
- porządkowanie zadań na osi **D‑2 → D‑1 → D0**,
- stały **status/sumę zmian** bez ręcznego klejenia,
- gotowe **prompty** i **reguły dla agenta**, aby proponował rozwiązania (np. brakujące materiały, ryzyka, priorytety).

Poniżej dostajesz **strukturę repo + proces pracy + YAML-e/templatki + prompty**. Wystarczy skopiować do GitHuba i podstawić swoje nazwy/sekrety.

---

## 2) Proponowana struktura repo
```
/
├─ README.md                         # krótki opis repo (1 ekran)
├─ docs/                             # materiały merytoryczne (PDF/MD/PNG)
│  ├─ PLAN_projektu_Las_Berlin_FINAL.md
│  ├─ LISTA_Materialy_i_Narzedzia_FINAL.md
│  ├─ project_summary.md
│  ├─ repository_analysis_report.md
│  ├─ *.pdf / *.png (mindmap, schematy)
│  └─ inbox/                         # nowo wrzucone pliki do przetworzenia
├─ prompts/                          # biblioteka promptów i reguł agenta
│  ├─ agent_rules.md
│  ├─ action_items_to_json.md
│  └─ personal-assistant-architecture.md
├─ agents/                           # workflowy (np. n8n), schematy
│  ├─ ai-agent-army.txt
│  ├─ ai agent army in n8n.pdf
│  └─ schemat_agenta.png
├─ ops/                              # automatyzacje lokalne (skrypty)
│  ├─ scripts/
│  │  ├─ doc_to_tasks.mjs            # wyciąganie zadań z .md/.pdf/.png
│  │  ├─ tasks_to_issues.mjs         # tworzenie issue z JSON
│  │  └─ summarize_status.mjs        # podsumowanie tygodnia/dnia
│  └─ settings.json                  # ustawienia narzędzi (np. mapy labeli)
├─ action_items/                     # wynik: zebrane zadania w JSON
│  └─ 2025-08-xx_meeting.json
└─ .github/
   ├─ ISSUE_TEMPLATE/
   │  ├─ task.yml
   │  └─ bug.yml
   ├─ workflows/
   │  ├─ create_issues_from_json.yml # automatyczne tworzenie Issue z JSON
   │  ├─ daily_summary.yml           # codzienne podsumowanie do docs/
   │  └─ lint_repo.yml               # styl MD, rozmiary, odnośniki
   └─ PULL_REQUEST_TEMPLATE.md
```

> **Zasada:** *docs/* zawiera treści merytoryczne; *prompts/* – jak z tych treści „wyciągać” zadania; *ops/* – skrypty; *action_items/* – wynik, który trafi do Issue; *.github/* – automaty.

---

## 3) GitHub Projects + Issues (workflow pracy)
**Tablica (Projects):**  
Kolumny: `Backlog` → `Ready` → `In progress` → `Review` → `Done` oraz swimlany `D‑2 | D‑1 | D0`.  

**Etykiety (labels):**
- `area:sciany`, `area:podwieszenia`, `area:wyspy`, `area:donice`  
- `day:D-2`, `day:D-1`, `day:D0`  
- `prio:P0`, `prio:P1`, `prio:P2`  
- `risk`, `blocked`, `doc`

**Issue template (skrót):**
```yaml
# .github/ISSUE_TEMPLATE/task.yml
name: Task
description: Jednostkowe zadanie
labels: ["prio:P2"]
body:
  - type: input
    id: context
    attributes:
      label: Kontekst
      placeholder: Np. Ścianki – panel A2
  - type: textarea
    id: steps
    attributes:
      label: Kroki
      description: Lista kroków (checklista)
  - type: dropdown
    id: day
    attributes:
      label: Dzień
      options: ["D-2", "D-1", "D0"]
  - type: labels
    id: area
    attributes:
      label: Obszar
      options: ["area:sciany","area:podwieszenia","area:wyspy","area:donice"]
```

---

## 4) Automaty z AI – co dostajesz od razu

### 4.1 „Doc → Tasks” (wyciąganie zadań z dokumentów)
- Wrzucasz pliki do `docs/inbox/` (PDF/MD/PNG).
- *ops/scripts/doc_to_tasks.mjs* czyta plik i – z pomocą promptów z `prompts/action_items_to_json.md` – zapisuje **JSON ze zdaniami** do `action_items/DATE.json`.

**Schemat JSON (zalecany):**
```json
{
  "source": "docs/inbox/PLAN_projektu_Las_Berlin_FINAL.md",
  "generated_at": "2025-08-26 01:54",
  "items": [
    {
      "title": "Wyciąć panele 50×100 dla ścianki S1",
      "area": "sciany",
      "day": "D-2",
      "priority": "P1",
      "checklist": ["Pomiary", "Cięcie", "QA"],
      "notes": "Zapas 10% materiału",
      "owner": null
    }
  ]
}
```

### 4.2 „Tasks → Issues” (tworzenie Issue z JSON)
Skrypt *ops/scripts/tasks_to_issues.mjs* uderza przez `gh` (GitHub CLI) i tworzy Issue z odpowiednimi labelami.  
> Dzięki temu jeden commit `action_items/*.json` = kilkanaście utworzonych Issue.

**Workflow (GitHub Actions):**
```yaml
# .github/workflows/create_issues_from_json.yml
name: Create issues from JSON
on:
  push:
    paths:
      - "action_items/*.json"
jobs:
  create:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm i
      - name: Create issues
        env:
          GH_TOKEN: ${{ secrets.GH_TOKEN }}
        run: node ops/scripts/tasks_to_issues.mjs
```

### 4.3 „Daily/Build Summary” (status projektu do `docs/`)
- Cron w Actions odpala *ops/scripts/summarize_status.mjs*.
- Skrypt czyta otwarte Issue/PR (przez `gh`), generuje **`docs/project_summary.md`** oraz (opcjonalnie) krótkie **changelog**.

```yaml
# .github/workflows/daily_summary.yml
name: Daily summary
on:
  schedule:
    - cron: "0 18 * * *"  # codziennie 18:00
jobs:
  summarize:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm i
      - name: Build summary
        env:
          GH_TOKEN: ${{ secrets.GH_TOKEN }}
          LLM_API_KEY: ${{ secrets.LLM_API_KEY }}   # klucz do wybranego LLM
        run: node ops/scripts/summarize_status.mjs
      - name: Commit summary
        run: |
          git config user.email "bot@users.noreply.github.com"
          git config user.name "project-bot"
          git add docs/project_summary.md
          git commit -m "chore: daily summary"
          git push
```

> **Uwaga o LLM:** Skrypty są celowo „dostawco-agnostyczne”. Ustaw `LLM_API_KEY` i `MODEL_ID` w *ops/settings.json*. Dzięki temu zmienisz provider bez ruszania kodu.

---

## 5) Prompty – gotowa biblioteka
### 5.1 „Action items z dokumentu” (skrót)
```
Jesteś PM instalacji zieleni. Wyciągnij z tekstu zadania atomowe w kategoriach: sciany, podwieszenia, wyspy, donice, logistyka.
Każde zadanie przypisz do D-2, D-1 lub D0 i oszacuj priorytet P0-P2.
Zwróć JSON wg schematu z prompts/action_items_to_json.md. Nie duplikuj. Dodaj checklistę 3-5 kroków.
```

### 5.2 „Asystent zakupów”
```
Na podstawie LISTA_Materialy_i_Narzedzia_FINAL.md wygeneruj listę pozycji do zakupu z ilościami (jeśli brak – oszacuj) i alternatywami.
Wyjście: tabela CSV (kolumny: kategoria, pozycja, ilość, jednostka, zamiennik A, zamiennik B, komentarz).
```

### 5.3 „Reviewer ryzyk”
```
Przejrzyj plan montażu i wskaż luki (BHP, nośności, okna dostaw, personel). Zaproponuj działania prewencyjne i plan awaryjny.
Wyjście: sekcja 'Ryzyka' do wklejenia w README (markdown, punktorami).
```

---

## 6) Zasady pracy i jakości
- **Branching:** `main` (chroniona) + `feature/…`; PR wymagają 1 review.  
- **Commity:** konwencja `feat|fix|docs|chore: …`.  
- **Kontrola plików:** duże binaria (PDF/PNG) lądują w `docs/`; README pozostaje krótkie.  
- **Wkład nowych osób:** tworzymy Issue z `good first issue` + `doc`.  
- **Bezpieczeństwo:** klucze (`LLM_API_KEY`, `GH_TOKEN`) trzymamy w **GitHub Secrets**.

---

## 7) Jak zacząć (Quickstart)
1. Utwórz repo → wrzuć obecne pliki do katalogów wg struktury z rozdz. 2.  
2. Skopiuj `.github/workflows/*.yml` i `ISSUE_TEMPLATE`.  
3. Dodaj **Secrets**: `GH_TOKEN`, `LLM_API_KEY`.  
4. `docs/inbox/` → dodaj nowe notatki/PDF/zdjęcia → commit.  
5. Po pipeline: sprawdź `action_items/*.json` i nowo utworzone **Issue**.  
6. Używaj tablicy **Projects** i labeli do zarządzania D‑2/D‑1/D0.

---

## 8) Rozszerzenia (opcjonalnie)
- **Konwersja PDF/PNG → MD** w pipeline (OCR + markdown).  
- **Auto‑tagowanie** Issue po słowach kluczowych (np. „keramzyt” → `area:donice`).  
- **Eksport do CSV** zakupów i integracja z arkuszem.  
- **Szablon wydruku D0** – 1 strona checków + plan stref.

---

## 9) FAQ (krótkie)
- *Czy muszę zmieniać prompty pod innego providera?* — Nie, ustaw tylko `MODEL_ID` i `LLM_API_KEY`.  
- *Czy Actions zrobią Issues automatycznie?* — Tak, po commicie do `action_items/*.json` lub po przetworzeniu plików z `docs/inbox/` gdy dodasz krok wywołujący `doc_to_tasks.mjs`.
- *Czy mogę wyłączyć AI i zostać przy ręcznym trybie?* — Tak; struktura repo i templatki będą dalej działać.

---

**Gotowe.** Po wrzuceniu tego przewodnika do repo (np. `README_GITHUB_PROJECT_GUIDE.md`) masz komplet procesu „dokument → zadania → Issues/Projects → podsumowania”, plus punkty zaczepienia pod dalsze automaty.
