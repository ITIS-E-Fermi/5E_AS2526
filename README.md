# 5E_AS2526
Repository del codice della classe 5E

# Tombola API

Overview

This document describes the REST API implemented in `server.js` (backend). The server listens on port 3001 by default.

Database (SQLite) tables

- users: { id, username, number, created_at }
- cards: { id, user_id, row, col, value }
- wins: { id, user_id, type, created_at }
- draws: { id, number, created_at }

Endpoints

- POST /join
  - Description: Register a new player with a card.
  - Request JSON:
    {
      "username": "string",    // optional, defaults to Player<N>
      "card": [[num,num,num,num,num],[...],[...]] // 3x5 array
    }
  - Response: 200 OK
    {
      "id": <userId>,
      "username": "...",
      "number": <playerNumber>,
      "card": [[...],[...],[...]]
    }
  - Example:

```bash
curl -X POST http://localhost:3001/join \
  -H "Content-Type: application/json" \
  -d '{"username":"Alice","card":[[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15]]}'
```

- GET /players
  - Description: Return all players with their cards, ordered by `number`.
  - Response: 200 OK
    [ { id, username, number, created_at, card: [[...],[...],[...]] }, ... ]

- POST /win
  - Description: Create a win record for a user.
  - Request JSON:
    { "user_id": <id>, "type": "Ambo|Terno|Quaterna|Cinquina|Tombola" }
  - Response: 200 OK
    { "id": <winId>, "user_id": <id>, "type": "..." }

- GET /wins
  - Description: List all wins with the winning username.
  - Response: 200 OK
    [ { id, username, type, created_at }, ... ]

- POST /checkWin
  - Description: Check whether a given user has a valid win based on supplied numbers. The endpoint validates extracted numbers, row membership and win hierarchy then records the win if valid.
  - Request JSON:
    {
      "username": "Alice",
      "numbers": [n1, n2, ...]  // numbers claimed by the user for the win
    }
  - Behavior / Rules (summary):
    - Verifies the `username` exists.
    - Ensures all provided `numbers` have already been drawn (exist in `draws`).
    - Valid numbers must belong to the same row of the user's card.
    - Determines win type by count:
      - 2 -> Ambo
      - 3 -> Terno
      - 4 -> Quaterna
      - 5 -> Cinquina
      - 15 -> Tombola (full card)
    - Prevents assigning a win of equal or lower rank than the most recent recorded win.
  - Responses:
    - 200 OK: { "message": "Vincita assegnata", "type": "..." }
    - 400 Bad Request: error messages for invalid numbers, not drawn, or lower/equal hierarchy
    - 404 Not Found: user not found
  - Example:

```bash
curl -X POST http://localhost:3001/checkWin \
  -H "Content-Type: application/json" \
  -d '{"username":"Alice","numbers":[2,3]}'
```

- POST /draw
  - Description: Draw a random number from 1..90 that has not yet been drawn and records it in `draws`.
  - Response: 200 OK
    { "number": <drawnNumber> }
  - Errors: 400 if all numbers already drawn.
  - Example:

```bash
curl -X POST http://localhost:3001/draw
```

- GET /draws
  - Description: Return the list of drawn numbers (ascending by created_at).
  - Response: 200 OK
    [ n1, n2, ... ]

- DELETE /reset
  - Description: Reset the database tables (delete all rows and reset AUTOINCREMENT counters) and in-memory counter.
  - Response: 200 OK
    { "message": "Database resettato con successo" }

Notes and tips

- The server uses an in-memory `counter` to assign incremental player `number`. A `DELETE /reset` resets it to 0.
- The `card` format expected by `/join` is a 3-element array of rows; each row should contain each cell value (the implementation stores `row` and `col`).

If you want, I can also:
- Produce an OpenAPI (Swagger) spec for this API.
- Convert this file to README style or translate to Italian.

