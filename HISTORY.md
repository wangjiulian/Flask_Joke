# CHANGELOG

## [v1.0.0]

### Added
- Implemented a minimal Flask API for searching, creating, deleting, and updating jokes.
- Structured the database using SQLite to persist jokes with a clear data model.
- Created RESTful API endpoints:
  - **GET /**: Fetch a random joke from a remote API.
  - **GET /api/jokes/?query={query}**: Search for jokes locally and remotely.
  - **POST /api/jokes/**: Add a new joke to the database.
  - **GET /api/jokes/{id}**: Retrieve a joke by its ID from local or remote sources.
  - **PUT /api/jokes/{id}**: Update an existing joke.
  - **DELETE /api/jokes/{id}**: Delete a joke by its ID.
- Added proper error handling for API endpoints.
- Included test cases to ensure the correctness of the API.
- Integrated Swagger documentation for better API usability.
- Set up CI/CD configuration with Docker for easy deployment.

### To-Do
- Optimize performance for database queries and update operations.
- Implement caching to reduce repeated calls to the remote API.
- Ensure data consistency during updates using mutex locks or optimistic locking.

### Notes
This version focuses on core functionality while maintaining simplicity and clarity in code. Future enhancements and features will build upon this foundation.