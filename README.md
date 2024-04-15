---
date: 2024-04-15T13:24:41.419258
author: AutoGPT <info@agpt.co>
---

# URL Shortener API

Based on the exchange, the task involves creating a URL shortening service with specified functional features and operational considerations. The service will need to accept a long URL as input, generate a unique, concise alias that is both easy to remember and includes a mix of letters and numbers, and store this alias alongside the original URL. Given the user's preferences, the alias format should aim for readability and uniqueness, incorporating strategies discussed such as appending numerical identifiers, using slugs derived from the original URL, or including timestamps for guaranteed uniqueness.

The shortened URLs can be either permanent or expire after a certain period, depending on the service provider's policy, emphasizing the need for flexibility in the system's design to accommodate different user preferences. Performance and scalability requirements suggest the system should be capable of handling a significant user load, including thousands of concurrent requests, with efficient database performance to ensure quick retrieval and storage of URL mappings.

Best practices for generating unique URL aliases and securely storing URL mappings in a database have been highlighted. These include using strong encryption, implementing proper access control, using hashing for sensitive mappings, and regular security audits. The tech stack selected for this project involves Python and FastAPI for the API framework, PostgreSQL for the database, and Prisma as the ORM, which supports these requirements.

An example of redirecting shortened URLs to their original URLs using FastAPI has been provided, demonstrating a basic implementation of the URL redirect feature. The system must also include endpoints for creating shortened URLs and retrieving the original URLs based on the shortened alias. Integrating these elements will meet the project's goals and ensure a scalable, secure, and user-friendly URL shortening service.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'URL Shortener API'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
