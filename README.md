## Mental Health Chatbot
[![License](https://img.shields.io/badge/license-Apache%202-blue)](LICENSE)

[Documentation](https://github.com/Aubrey6/INFO7375Final_Mental_Health_RAG_ChatBot/blob/main/Final%20Project%20Doc.pdf)

[Video](https://youtu.be/4nFkjlUvFRU)

### Overview
This project provides a document-based question-answering system that uses OpenAI embeddings and FAISS for efficient document retrieval and answer generation. The system is designed to:

1. Preprocess and vectorize documents in a specified directory.
2. Store document vectors in a FAISS vector store.
3. Support multi-turn conversations and query documents to generate answers to user questions.

The core components of the project are implemented using Python, Streamlit for the user interface, OpenAI for embedding generation, and FAISS for efficient vector-based search and retrieval.

### Table of Contents
- [Project Structure](#project-structure)  
- [Dependencies](#dependencies)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [How It Works](#how-it-works)

### Project Structure
```
/project-root  
│  
├── /documents                    # Folder containing the documents to be processed  
├── ├── embedd.json               # File recording vectorized document metadata
├── /vector_store                 # Folder for storing the FAISS vector index
├── app.py                        # Main application file (Streamlit interface)
├── Prompts.py                    # Containing predefined prompt templates
└── embeddings.py                 # Script for generating document embeddings
```

### Dependencies
To run the project, you need to install the following dependencies:
- langchain
- langchain-community
- langchain-openai
- faiss-cpu
- streamlit
- python-dotenv

You can install all the dependencies by running:
```bash
pip install langchain langchain-community langchain-openai faiss-cpu streamlit python-dotenv
```

### Setup Instructions
1. Obtain OpenAI API Key:
To use OpenAI's embedding model, you'll need an API key. Obtain your key from OpenAI's API.

2. Configure Environment:
Set up your OpenAI API key in your environment. You can do this by setting the OPENAI_API_KEY in your environment variables or write them in `.env` use key `OPENAI_API_KEY`.

3. Prepare Documents:
Place your documents (.txt, separate by '\n\n') in the documents/ directory.

4. Run Vectorization:
To preprocess and vectorize your documents, run the following command:

```bash
python ./embedding.py
```
This will traverse all documents in the documents/ folder, check if they are already vectorized, and perform vectorization if necessary. The generated embeddings are stored in the FAISS vector store.

5. Run the Application:
To start the Streamlit interface and interact with the question-answering system, run:

```bash
streamlit run app.py
```

### Usage
1. Interface:
Once the app is running, open the Streamlit interface in your web browser. You will see some input boxes where you can:
   - Select a Large Language Model (LLM) for the question-answering process.
   - Input a question.

2. Question-Answer Flow:
   - When a user submits a question, the system uses the selected LLM and chat history to process the input and generates a new question if necessary.
   - The FAISS index is then queried for the most similar document vectors to the question.
   - The relevant document fragments are retrieved, processed by the predefined prompt template, and used to generate an answer.
   - The final answer is displayed in the Streamlit interface by stream output.

3.Multi-Turn Conversations:
    - The system supports multi-turn conversations by maintaining chat history, which can be used to generate contextually relevant follow-up questions and answers.

### How It Works
1. Text Preprocessing and Vectorization
   - Traverse Documents:
   The program traverses all the documents in a specified directory (docs/) and checks whether each document has been vectorized already by referencing the embedded.json file.

   - Check Embedding Records:
   For already vectorized documents, the information is recorded in embedded.json. If a document is listed, it is skipped in the next run; otherwise, it proceeds to vectorization.

   - Vectorization:
   Documents that are not vectorized are processed by the OpenAI embeddings model, generating vector representations of the documents.

   - FAISS Vector Store Handling:
   The system checks whether a FAISS vector store already exists. If it does, it loads the existing store; if not, it creates a new FAISS index to store the embeddings.

   - Store Vectors:
   The vectorized document embeddings are stored in the FAISS vector store for fast and efficient retrieval during querying.


2. Question-Answer Processing
   - User Interaction:
   The user selects an LLM and submits a question via the Streamlit interface (app.py).

   - Conversation Management:
   The system maintains chat history to handle multi-turn conversations, enabling the generation of new questions based on the conversation context.

   - Embedding Model Processing:
   The input question is processed using the OpenAI embedding model. The question embedding is then compared with document embeddings stored in FAISS to find the most relevant results.

   - Document Retrieval:
   FAISS retrieves the closest matching document vectors based on the similarity to the input question.

   - Answer Generation:
   The retrieved document fragments are passed through a predefined prompt template (from prompts.py), which processes the text and generates an answer using the LLM.

   - Answer Display:
   The answer generated by the LLM is then displayed to the user on the Streamlit interface.

Feel free to reach out for any issues or suggestions regarding the project. Enjoy using the document-based question-answering system!

## License This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
