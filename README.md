# Iris Full-Stack Classifier

- **Description:** Extend the FastAPI Iris classifier with a web UI and PostgreSQL inference logging, all runnable with Docker Compose.
- **Inputs:** Sepal length, sepal width, petal length, and petal width in centimetres.
- **Classes:** Setosa, versicolor, and virginica.

## Assignment

- Create a `ui/` directory with a Streamlit app for entering the four measurements.
- Send the measurements from the UI to the API's `POST /predict` endpoint and display the predicted species.
- Add a `ui/Dockerfile` to build and run the Streamlit app.
- Add a root-level `compose.yaml` with services for the API, UI, and PostgreSQL.
- Use the lightweight official PostgreSQL image `postgres:16-alpine` and configure a persistent data volume.
- Create `api/.env` with a `DATABASE_URL` for the Compose PostgreSQL service, for example:
  `DATABASE_URL=postgresql://postgres:postgres@db:5432/iris`
- Keep the database name, user, and password consistent between `api/.env` and the Compose PostgreSQL settings.
- Configure the UI to call the API at `http://api:8000` from inside Compose; use the Compose service name, not `localhost`.
- Start the full stack from the project root with `docker compose up --build`.
- Verify the UI prediction, API docs at `http://localhost:8000/docs`, and inference records in PostgreSQL.

## Run the stack

Requirements: Docker with Docker Compose (on Windows, Docker Desktop with WSL 2).
Ports 8000 and 8501 must be free.

From the project root:

```bash
docker compose up --build
```

This starts three services:

| Service | Description | Address |
|---|---|---|
| `ui` | Streamlit web app | <http://localhost:8501> |
| `api` | FastAPI classifier | <http://localhost:8000/docs> |
| `db` | PostgreSQL 16 | reachable only inside Compose as `db:5432` |

The API waits for the database to be healthy, then creates the `inferences`
table if it does not exist.

## Make a prediction

Open the UI at <http://localhost:8501>, enter the four measurements, and press
**Predict**. You can also call the API directly (bash):

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"feature_array":[5.1,3.5,1.4,0.2]}'
```

In Windows PowerShell:

```powershell
Invoke-RestMethod -Uri http://localhost:8000/predict -Method Post `
  -ContentType 'application/json' -Body '{"feature_array":[5.1,3.5,1.4,0.2]}'
```

Expected response (the `class_id ` key has a trailing space):

```json
{"prediction":{"class_id ":0,"class_name":"setosa"}}
```

## Check the database

While the stack is running, from the project root:

```bash
docker compose exec db psql -U postgres -d iris -c "SELECT * FROM inferences;"
```

Each prediction adds one row with `id`, `sepal_length`, `sepal_width`,
`petal_length`, `petal_width`, `predicted_species`, and `created_at`.

## Stop the stack

```bash
docker compose down
```

The data is kept in the `pgdata` volume. To delete it as well, run
`docker compose down -v`.

## Configuration

- `api/.env` sets `DATABASE_URL` for the API. Its user, password, and database
  name must match the `POSTGRES_*` values in `compose.yaml`. The file is
  committed because the assignment requires it; these credentials are for local
  use only.
- `API_URL` tells the UI where the API is. It defaults to `http://api:8000`.
