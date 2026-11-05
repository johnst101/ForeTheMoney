# ForeTheMoney Glossary

This glossary defines the shared domain language used in product and infrastructure discussions for the project.

## ForeTheMoney
The golf pool application that tracks weekly player picks and season-long PGA Tour earnings.

## Environment
A runtime context for the application, such as local development, stage, or production. Each environment has its own database connection and secret values.

## Local environment
The developer workstation setup used for building and testing the app without affecting staging or production.

## Stage environment
The pre-production deployment used to validate changes before they reach end users. It should use a dedicated database branch and deployment configuration.

## Production environment
The live deployment used by real users. It must be the most stable and protected environment.

## Secret
A sensitive configuration value, such as a database connection string or JWT signing key, that should not be stored in source control.

## Parameter Store
AWS Systems Manager Parameter Store, used to hold environment-specific secrets securely and retrieve them at runtime.

## Deployment blueprint
The implementation-level specification describing how the app is packaged, deployed, configured, and run in a given environment.

## Service
A runnable backend process or container responsible for serving the application.

## Reverse proxy
A front-facing server, such as Nginx, that accepts traffic on standard ports and forwards requests to the backend service.

## Health check
A lightweight endpoint or probe used to confirm that the application is accepting traffic and is healthy enough to serve requests.

## Database branch
A separate database instance or logical environment for a given deployment context, such as a Neon branch for stage or prod.
