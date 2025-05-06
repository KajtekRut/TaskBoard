# TaskBoard – Prosty system zarządzania zadaniami

TaskBoard to lekka aplikacja backendowa stworzona z wykorzystaniem **FastAPI**, która umożliwia użytkownikom tworzenie projektów i zarządzanie zadaniami w czasie rzeczywistym. Dzięki integracji z WebSocket użytkownicy otrzymują natychmiastowe powiadomienia o nowych zadaniach.

---

## Funkcjonalności

- Rejestracja i logowanie użytkowników z wykorzystaniem JWT
- CRUD dla projektów (`Project`)
- CRUD dla zadań (`Task`) przypisanych do projektów
- Powiadomienia w czasie rzeczywistym (WebSocket) o nowych zadaniach
- Konteneryzacja aplikacji za pomocą Docker i Docker Compose

---

## Modele danych

- **User** – dane uwierzytelniające (email, hasło, token)
- **Project** – projekt użytkownika (nazwa, opis)
- **Task** – zadania przypisane do projektów (nazwa, status, termin)

---

## Autentykacja

- Tokeny JWT
- Endpointy:
  - `POST /register` – rejestracja nowego użytkownika
  - `POST /login` – logowanie i pobranie tokenu

---

## Endpointy API

### Projekty (`Project`)
- `GET /projects/` – pobierz projekty zalogowanego użytkownika
- `POST /projects/` – utwórz nowy projekt
- `PUT /projects/{id}` – edytuj projekt
- `DELETE /projects/{id}` – usuń projekt

### Zadania (`Task`)
- `GET /tasks/` – pobierz zadania użytkownika
- `POST /tasks/` – utwórz nowe zadanie
- `PUT /tasks/{id}` – edytuj zadanie
- `DELETE /tasks/{id}` – usuń zadanie

---

## WebSocket

- `ws://localhost:8000/ws/notifications`
- Po połączeniu użytkownik otrzymuje powiadomienia, gdy dodane zostanie nowe zadanie do jego projektu.

---

## Konteneryzacja

Aplikacja gotowa do uruchomienia w kontenerach Dockera:

### Struktura:
- `Dockerfile` – buduje backend FastAPI
- `docker-compose.yml` – uruchamia backend i bazę danych (np. PostgreSQL)

### Uruchomienie:
```bash
docker-compose up --build
