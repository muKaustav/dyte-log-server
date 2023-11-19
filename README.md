<h1 align="center">Dyte Backend Task 🧭</h1>

## 📚 | Problem Statement

- Develop a log ingestor system that can efficiently handle vast volumes of log data.
- Offer a simple interface for querying this data using full-text search or specific field filters.
- The logs should be ingested (in the log ingestor) over HTTP, on port `3000`.

### Log Ingestor:

- Develop a mechanism to ingest logs in the provided format.
- Ensure scalability to handle high volumes of logs efficiently.
- Mitigate potential bottlenecks such as I/O operations, database write speeds, etc.
- Make sure that the logs are ingested via an HTTP server, which runs on port `3000` by default.

### Query Interface:

- Offer a user interface (Web UI or CLI) for full-text search across logs.
- Include filters based on:
  - level
  - message
  - resourceId
  - timestamp
  - traceId
  - spanId
  - commit
  - metadata.parentResourceId
- Aim for efficient and quick search results.

<br/>

## 📝 | Sample Queries

The following are some sample queries that will be executed for validation.

- Find all logs with the level set to "error".
- Search for logs with the message containing the term "Failed to connect".
- Retrieve all logs related to resourceId "server-1234".
- Filter logs between the timestamp "2023-09-10T00:00:00Z" and "2023-09-15T23:59:59Z". (Bonus)

## 🌐 | Test Project

- Clone this repository.
- Install Docker Desktop.
- Run `docker-compose up` in the root directory of the project.
- The Web UI will be available at `http://localhost:3000/`.

### Note:
- The Web UI is very basic, and is only meant for testing the API.

#### Demo Link hosted on GDrive: [Click Here]()

<br/>

## 🧑🏽 | Author

**Kaustav Mukhopadhyay**

- Linkedin: [@kaustavmukhopadhyay](https://www.linkedin.com/in/kaustavmukhopadhyay/)
- Github: [@muKaustav](https://github.com/muKaustav)

<br/>

---
