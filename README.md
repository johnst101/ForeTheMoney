# ForeTheMoney
A golf pool web app where players select 6 golfers from weekly tiers and compete by accumulating real PGA Tour earnings throughout the season.

## Overview
<!-- Briefly explain the app's purpose, target users, and core game loop in 3-5 sentences. -->

## Features
<!-- List key product capabilities (for example: weekly picks, tier validation, leaderboard tracking, season totals). -->

## Tech Stack
<!-- Summarize major technologies used by layer: backend framework, ORM, database, migrations, and any planned frontend stack. -->

## Project Structure
<!-- Add a short tree or bullets describing the most important folders and what each one owns. -->

## Getting Started
<!-- Explain prerequisites (Python version, PostgreSQL, etc.) and how to clone/open the project. -->

## Backend Setup
<!-- Provide exact setup commands: install dependencies, configure environment variables, run database startup, and apply migrations. -->

## Running the App
<!-- Show how to start the API locally and where to access docs/endpoints (for example: Swagger/OpenAPI URL). -->

## Database
<!-- Document connection details, migration workflow, and any seed/init strategy for local development. -->

## API Notes
<!-- Add a high-level list of core routes/resources and expected request/response behavior. -->

## Testing
<!-- Describe how to run tests, what test types exist, and current coverage expectations. -->

## Configuration

The application relies on environment variables for runtime configuration. The current contract is:

- `APP_ENV` — identifies the runtime environment (`local`, `stage`, or `prod`)
- `DATABASE_URL` — the database connection string for the active environment; use the PostgreSQL URL format expected by the installed driver, currently `postgresql+psycopg2://...`
- `SECRET_KEY` — JWT signing key used for authentication
- `ALGORITHM` — the JWT algorithm used to sign tokens
- `ACCESS_TOKEN_EXPIRE_DAYS` — lifetime of JWT access tokens in days

For local development, values can be stored in `.env` or `.env.example`.

For AWS deployment, the preferred pattern is to store these values in AWS Systems Manager Parameter Store under the project namespace:

- `/forethemoney/stage/DATABASE_URL`
- `/forethemoney/stage/SECRET_KEY`
- `/forethemoney/stage/ALGORITHM`
- `/forethemoney/stage/ACCESS_TOKEN_EXPIRE_DAYS`
- `/forethemoney/prod/DATABASE_URL`
- `/forethemoney/prod/SECRET_KEY`
- `/forethemoney/prod/ALGORITHM`
- `/forethemoney/prod/ACCESS_TOKEN_EXPIRE_DAYS`

This keeps secrets out of source control and makes the app environment-aware without changing the runtime contract.

## Roadmap
<!-- Capture near-term and long-term planned features to show project direction. -->

## Contributing
<!-- Outline contribution workflow (branching, PR expectations, code style, and review process). -->

## License
<!-- State the project license and point to the LICENSE file. -->
