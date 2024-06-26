# Source-Code-Analyzer

## Overview

In today's software development landscape, understanding and navigating large and complex codebases is a significant challenge faced by developers worldwide. This problem is particularly pronounced for new team members joining a project, as well as for experienced developers working on unfamiliar codebases.

Source Code Analyzer is an end-to-end solution designed to facilitate understanding and querying of large and complex codebases. Leveraging cutting-edge technologies including OpenAI embeddings, Gemini 1.5, Pinecone, Flask, and MongoDB, this application aims to empower developers by providing a robust platform for analyzing and querying source code repositories hosted on GitHub.

## Core Technologies Used

- **OpenAI**: Utilized for generating embeddings of code snippets.
- **Gemini**: Integrated as the core language model for responding to user queries.
- **Pinecone**: Used for storing and retrieving embeddings efficiently.
- **Flask**: Employed to develop the web interface and handle user interactions.
- **MongoDB**: Utilized for storing metadata and managing user sessions.

## Installation

1. Clone this repository using `git clone https://github.com/Sandeep-Pasumarthi/Source-Code-Analyser.git`.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Set up MongoDB and ensure it is running locally or on a remote server.
4. Obtain API keys for OpenAI, Pinecone and Gemini set them as environment variables.
5. Create a .env file.
```
GOOGLE_API_KEY="*****YOUR KEY HERE*****"
GEMINI_CHAT_MODEL="models/gemini-1.5-pro"
PINECONE_API_KEY="*****YOUR KEY HERE*****"
PINECONE_INDEX="source-code-analyser"
PINECONE_TEXT_KEY="page_content"
OPENAI_API_KEY="*****YOUR KEY HERE*****"
EMBEDDING_MODEL="text-embedding-3-large"

MONGO_URI="mongodb+srv://<Your MongoDB URL>"
DB="Source_Code_Analyser"
LOGIN_COLLECTION="users"
DASHBOARD_COLLECTION="conversation_titles"
USER_ID_LEN=30
CONVERSATION_ID_LEN=15
```
6. Run `python app.py` to start the Flask server.
7. Access the application at `http://localhost:5000`.

## Usage

1. Navigate to the web interface.
2. Login/Signup using your credentials. If you don't want to, use **"test@gmail.com"** and password **"test"**.
3. Upload a source code repository URL from GitHub in the dashboard page or select a previously uploaded repository.
4. Enter your queries using natural language.
5. Receive responses generated by Gemini 1.5 based on the codebase.

## UI Considerations

As the primary focus of this project is on functionality and backend development, please note that the user interface may not be as polished or visually appealing as other applications. While efforts have been made to provide a user-friendly experience, UI design is not the primary expertise of me. Therefore, users should expect a basic and utilitarian interface that prioritizes functionality over aesthetics.