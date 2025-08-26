# Szczegółowa Analiza Repozytorium - Sovereign Intelligence

## Przegląd Projektu
Repozytorium **Sovereign Intelligence** to system automatyzacji zarządzania projektami wykorzystujący AI (Large Language Models) do przetwarzania transkrypcji spotkań i integracji z GitHub Projects.

## Struktura Katalogów i Plików

### 📁 **agent_config/** - Konfiguracja Agentów AI
Katalog zawierający konfigurację i prompty dla agentów AI.

#### 📄 **agent_rules.md** (807B, 11 linii)
- **Zawartość**: Zasady i wytyczne dla agentów AI
- **Kluczowe funkcje**:
  - Definiuje workflow: prompty → dane → taski → dokumentacja
  - Określa preferowane modele LLM dla różnych zadań:
    - **Ekstrakcja danych**: Claude, GPT-4, Llama3-70B, Bielik-7B
    - **Podsumowania po polsku**: Bielik, Llama3-70B, Command R+
    - **Kodowanie**: GPT-4, Claude Opus, Llama3-70B-Code
  - Wymaga aktualizacji dokumentacji po każdej zmianie

#### 📄 **settings.json** (228B, 8 linii)
- **Zawartość**: Konfiguracja domyślnych modeli językowych
- **Ustawienia**:
  - `default_language_model`: "bielik-7b"
  - `fallback_model`: "llama3-70b"
  - `summarization_model`: "bielik-7b"
  - `data_extraction_model`: "gpt-4"
  - `code_generation_model`: "gpt-4"

#### 📁 **prompts/** - Katalog Promptów
##### 📄 **action_items_to_json.md** (463B, 7 linii)
- **Cel**: Ekstrakcja zadań z tabeli "Action Items" w raportach Markdown
- **Funkcja**: Konwersja do JSON z polami: title, assignee, due_date, priority
- **Format wyjściowy**: Czysty JSON array bez dodatkowego tekstu

##### 📄 **project_summary.md** (275B, 6 linii)
- **Cel**: Podsumowanie notatek ze spotkań projektowych
- **Elementy**: Decyzje, ryzyka, kluczowe zadania
- **Język**: Polski z formatowaniem Markdown

### 📁 **data/** - Dane i Przykłady
Katalog zawierający przykładowe dane i wyniki przetwarzania.

#### 📄 **sample_report.md** (385B, 7 linii)
- **Zawartość**: Przykładowy raport z tabelą "Action Items"
- **Struktura**: Tabela z kolumnami: Zadanie, Kto?, Kiedy?, Priorytet
- **Przykładowe zadania**:
  - Przygotować środowisko (Jan Kowalski, 2024-09-01, Wysoki)
  - Skonfigurować Whisper (Anna Nowak, 2024-09-03, Średni)
  - Testy integracyjne (brak przypisania, 2024-09-10, Niski)

#### 📄 **sample_tasks.json** (393B, 20 linii)
- **Zawartość**: JSON z zadaniami wyekstrahowanymi z raportu
- **Struktura**: Array obiektów z polami title, assignee, due_date, priority
- **Obsługa wartości null**: Dla brakujących danych

### 📁 **docs/** - Dokumentacja
#### 📄 **README.md** (1.2KB, 25 linii)
- **Cel**: Główna dokumentacja projektu
- **Zawartość**:
  - Opis funkcji systemu
  - Struktura repozytorium
  - Instrukcje użycia
  - Wskazówki dotyczące modeli LLM
- **Workflow**: Markdown → JSON → GitHub Projects

### 📁 **project/** - Plany i Architektura
#### 📄 **architecture.md** (386B, 7 linii)
- **Zawartość**: Architektura systemu
- **Komponenty**:
  - Moduł ekstrakcji danych z Markdown
  - Moduł integracji z GitHub Projects
  - Modularny katalog promptów
  - Konfiguracja modeli LLM
- **Cel**: Dokumentowanie decyzji architektonicznych

#### 📄 **plan.md** (335B, 7 linii)
- **Zawartość**: Plan rozwoju projektu
- **Etapy rozwoju**:
  1. Konwersja Action Items z Markdown do JSON
  2. Automatyczny import do GitHub Projects
  3. Modularny dobór promptów i modeli
  4. Interfejs zarządzania workflow
  5. Integracja z Obsidian

### 📁 **src/** - Kod Źródłowy
#### 📄 **markdown_to_json.py** (1.4KB, 38 linii)
- **Cel**: Konwersja raportów Markdown do JSON
- **Funkcje**:
  - `extract_action_items()`: Parsowanie tabeli Markdown
  - Regex do ekstrakcji danych z tabeli
  - Obsługa brakujących wartości (null)
- **Użycie**: `python src/markdown_to_json.py <input_md> <output_json>`

#### 📄 **github_projects.py** (1010B, 28 linii)
- **Cel**: Podstawowa integracja z GitHub Projects (Classic)
- **Funkcje**:
  - `create_project_item()`: Tworzenie kart w projekcie
  - Używa GitHub API v3
  - Konfiguracja przez zmienne środowiskowe
- **Status**: TODO - załadowanie zadań z JSON

#### 📄 **github_projects_importer.py** (2.1KB, 60 linii)
- **Cel**: Zaawansowany importer do GitHub Projects
- **Funkcje**:
  - Obsługa Projects Classic i Beta
  - `github_projects_beta_create_issue()`: GraphQL API dla Beta
  - `github_projects_classic_create_card()`: REST API dla Classic
  - `import_tasks()`: Główna funkcja importująca
- **Konfiguracja**: Zmienne środowiskowe (.env)

### 📁 **.github/workflows/** - Automatyzacja CI/CD
#### 📄 **import-tasks.yml** (595B, 24 linii)
- **Cel**: Automatyczny import zadań przy zmianach
- **Trigger**: Push do `project/tasks.md` lub `data/example_report.md`
- **Akcje**:
  - Setup Python 3.10
  - Instalacja dependencies
  - Uruchomienie skryptu importu
- **Secrets**: PERSONAL_TOKEN, PROJECT_ID

### 📄 **requirements.txt** (22B, 2 linii)
- **Zależności**:
  - `requests`: HTTP requests dla GitHub API
  - `python-dotenv`: Zarządzanie zmiennymi środowiskowymi

## Analiza Techniczna

### Architektura Systemu
1. **Modularny design** z separacją konfiguracji, kodu i danych
2. **Obsługa wielu modeli LLM** z automatycznym doborem
3. **Integracja z GitHub Projects** (Classic i Beta)
4. **Automatyzacja CI/CD** przez GitHub Actions

### Workflow
1. **Input**: Raport Markdown z tabelą Action Items
2. **Processing**: Ekstrakcja przez LLM lub parser
3. **Output**: JSON z zadaniami
4. **Integration**: Import do GitHub Projects
5. **Documentation**: Aktualizacja planów i dokumentacji

### Mocne Strony
- ✅ Dobrze zorganizowana struktura katalogów
- ✅ Modularny system promptów
- ✅ Obsługa różnych modeli LLM
- ✅ Automatyzacja CI/CD
- ✅ Dokumentacja w języku polskim

### Obszary do Rozwoju
- 🔄 Interfejs użytkownika (n8n/Streamlit)
- 🔄 Integracja z Obsidian
- 🔄 Obsługa błędów i walidacja
- 🔄 Testy jednostkowe
- 🔄 Logowanie i monitoring

## Podsumowanie
Repozytorium przedstawia solidną podstawę dla systemu automatyzacji zarządzania projektami z wykorzystaniem AI. Projekt ma jasno zdefiniowaną architekturę, modularny design i dobrze przemyślany workflow. Główne funkcjonalności są zaimplementowane, a system jest gotowy do dalszego rozwoju zgodnie z planem w `project/plan.md`.
