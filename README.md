# Library Management API

This project implements a simple API for a library information system. The API is designed to be used by library staff to track and update the status of books in the library's collection.

## Features

The API provides the following functionality:

- **Add a new book**: Allows staff to add a new book to the library's collection. Each book is identified by a unique serial number, a title, an author, and its current status (whether it is currently borrowed or available).
  
- **Remove a book**: Enables the deletion of a book from the library's collection.

- **Retrieve a list of all books**: Returns a list of all books in the library, including their details and status.

- **Update book status**: Allows staff to update the status of a book, marking it as either borrowed or available. When a book is borrowed, the API also records the borrower's library card number and the date of borrowing.

## Data Model

Each book in the library contains the following information:

- **Serial Number**: A unique six-digit identifier for the book (e.g., `123456`).
- **Title**: The title of the book.
- **Author**: The author of the book.
- **Borrowed Status**: Indicates whether the book is currently borrowed. If borrowed, additional details such as the borrower's six-digit library card number and the date of borrowing are stored.

## Technical Stack

- **Framework**: Implemented using FastAPI web framework 
- **Database**: PostgreSQL is used for storing book information.
- **Containerization**: The application is containerized using Docker, with the setup managed via `docker-compose`.

## Running the Application

To run the application, ensure Docker and Docker Compose are installed, then execute the following command:

```bash
docker compose up
```