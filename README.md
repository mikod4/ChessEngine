# ChessEngine

> Projekt na przedmiot Języki Skryptowe.

**ChessEngine** to aplikacja desktopowa napisana w Pythonie umożliwiająca grę w szachy pomiędzy dwoma graczami lub graczem oraz komputerem. Algorytmy grające w szachy można wybrać przed startem partii oraz w trakcie gry.

## Instalacja i kompilacja

Aplikacja może być uruchamiana z użyciem pythona(program był testowany na wersji 3.14.15) oraz zainstalowanych modułów określonych w pliku requirements.txt. 
```bash
python3 main.py
```

Można również skompilować aplikację na swój system operacyjny z użyciem modułu pyinstaller oraz dostarczonego skryptu ChessEngine.spec

> ⚠️ PyInstaller kompiluje aplikację **wyłącznie dla systemu operacyjnego, na którym jest uruchamiany** — cross-kompilacja nie jest wspierana.

**1. Instalacja zależności deweloperskich**

Upewnij się, że jesteś wewnątrz wirtualnego środowiska projektu, a następnie zainstaluj wszystkie potrzebne zależności:

```bash
pip install -r requirements.txt
```

**2. Kompilacja przy użyciu pliku `.spec`**

W katalogu głównym projektu uruchom:

```bash
pyinstaller ChessEngine.spec
```

**3. Lokalizacja pliku wynikowego**

Po zakończeniu kompilacji gotowa aplikacja (wraz ze wszystkimi zasobami — grafiką i dźwiękami) znajdzie się w:

```
/dist/ChessEngine/
```

Dodatkowo tworzony jest katalog `/build/` z plikami pośrednimi.

---

## Funkcjonalności

### Układ interfejsu

Interfejs podzielony jest horyzontalnie na trzy sekcje:

```
┌─────────────┬──────────────────┬──────────────────┐
│   Wskaźnik  │   Szachownica    │  Historia ruchów │
│    oceny    │    (centrum)     │   (notacja PGN)  │
│  (po lewej) │                  │   (po prawej)    │
└─────────────┴──────────────────┴──────────────────┘
```

**Wskaźnik oceny** — pionowy pasek graficzny pokazujący matematyczną przewagę pozycyjną w czasie rzeczywistym.

**Szachownica** — główny obszar gry z obsługą kliknięć myszką do wybierania i przesuwania figur.

**Historia ruchów** — automatyczna, chronologiczna rejestracja posunięć w oficjalnej notacji szachowej.

---

### Interaktywne funkcje

| Funkcja | Opis |
|---------|------|
| Podświetlanie pól | Po zaznaczeniu figury wyświetlane są wszystkie legalne ruchy |
| Ostatni ruch | Stale widoczne zaznaczenie ostatnio wykonanego posunięcia |
| Szach | Pole pod zagrożonym królem podświetlane na czerwono |
| Promocja pionka | Okno dialogowe wyboru figury po dotarciu do ostatniej linii |
| System audio | Dźwięki dla ruchów, bić, roszad, szachów i nielegalnych posunięć |

---

### Opcje konfiguracji (menu górne)

**Gra**
- Zapis i wczytywanie pozycji z plików w formacie **FEN**
- Szybki restart partii

**Bot**

| Tryb | Opis |
|------|------|
| Lokalny (2 graczy) | Gra dwóch osób na jednym komputerze |
| Random | Bot wykonujący losowe legalne ruchy |
| Minimax (głębokość 3) | AI z analizą 3 ruchów w przód |
| Minimax (głębokość 5) | AI z analizą 5 ruchów w przód |

**Kolor & Pokaż**
- Obracanie szachownicy
- Ukrywanie paska oceny i historii ruchów

---

## Architektura techniczna

Aplikacja zaprojektowana w oparciu o wzorzec **MVC (Model-View-Controller)**, który zapewnia całkowite odseparowanie logiki gry od interfejsu graficznego.

### Warstwy architektury

#### Model — `ChessModel`

Reprezentuje stan danych i logikę biznesową gry.

- Bazuje na bibliotece **python-chess**
- Przechowuje aktualną pozycję w notacji FEN
- Odpowiada za weryfikację legalności posunięć
- Wykrywa stany końca gry: mat, pat, remis przez trzykrotne powtórzenie pozycji
- Nie posiada żadnej wiedzy o interfejsie graficznym

#### View — `MainWindow`, `Board`, `Sidebar`, `EvaluationBar`

Warstwa prezentacji oparta na frameworku **PyQt6**.

- Rysuje szachownicę, figury oraz inne elementy wizualne na szachownicy takie jak oznaczony szach, dostępne legalne ruchy
- Wyświetla menu górne i okna dialogowe (popup)
- Rejestruje zdarzenia fizyczne (kliknięcia myszką) i przekazuje je do kontrolera
- Nie modyfikuje samodzielnie stanu gry

#### Controller — `GameController`

Mózg operacyjny aplikacji — pośrednik między Modelem a Widokiem.

- Przechwytuje sygnały kliknięć z warstwy widoku
- Odpytuje Model o legalność ruchu
- Po zatwierdzeniu posunięcia — wysyła instrukcje aktualizacji grafiki i odtworzenia dźwięku

---

### Komunikacja — Signals & Slots

Wewnętrzna komunikacja odbywa się asynchronicznie i zdarzeniowo za pomocą mechanizmu sygnałów Qt (`pyqtSignal`). Dzięki temu komponenty nie są ze sobą sztywno sprzężone.

```
[Użytkownik klika pole]
        ↓
   View emituje sygnał
        ↓
  Controller przechwytuje
        ↓
   Model weryfikuje ruch
        ↓
Controller emituje board_updated(fen)
        ↓
   View aktualizuje grafikę
```

---

### Współbieżność — wątek bota

Obliczenia algorytmu Minimax (zwłaszcza na głębokości 5) są intensywne obliczeniowo. Aby uniknąć zamrożenia interfejsu, proces decyzyjny bota działa w osobnym wątku tła.

```
Główny wątek GUI
        │
        ├──► BotWorker (QThread)
        │         │
        │    [obliczenia Minimax]
        │         │
        └◄── sygnał z wybranym ruchem
```

Klasa `BotWorker` dziedziczy po `QThread`. Po zakończeniu obliczeń bot wysyła sygnał zwrotny z wybranym posunięciem, co gwarantuje pełną płynność interfejsu przez całą rozgrywkę.

---
