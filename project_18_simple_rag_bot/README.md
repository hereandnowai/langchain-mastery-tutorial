# Project 18: Simple RAG Bot

**Objective:** To build a basic Retrieval-Augmented Generation (RAG) bot.

**`main.py`:**
*   Load a `knowledge_base.txt`.
*   Use `RecursiveCharacterTextSplitter` to chunk the document.
*   Use `FAISS` and `GoogleGenerativeAIEmbeddings`.
*   Create a retrieval chain.

**`knowledge_base.txt`:** A slightly longer document with more detailed information.

**`README.md`:** Explain the concept of RAG and why it's powerful for reducing hallucinations and using up-to-date information.

**Real-World Value:** RAG is a powerful technique for building chatbots and QA systems that can answer questions about a specific domain of knowledge. This is useful for customer support, internal knowledge bases, and more.