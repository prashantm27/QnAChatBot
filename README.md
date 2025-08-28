## 📄 GenAI Document Question Answering App **QnAChatBot**

This project is a Generative AI-based application that allows users to ask questions and receive answers from uploaded documents. It leverages state-of-the-art language models and provides a simple, interactive interface built with Streamlit.

🚀 Features

📚 Upload and parse documents (PDF)

❓ Ask natural language questions about the content

💬 Get accurate answers generated using large language models

⚡ Fast and user-friendly Streamlit web interface

🛠️ Installation

Clone the repository

git clone https://github.com/prashantm27/QnAChatBot.git
cd QnAChatBot

Create and activate a virtual environment (optional but recommended)

python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate


Install dependencies

pip install -r requirements.txt

▶️ Running the Application

Once the dependencies are installed, you can launch the Streamlit app using:

streamlit run app.py

Folder Structure
.
├── app.py                  # Main Streamlit application
├── prompts.py              # Prompts 
├── vector_db.py            # vector db operations
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation
├── uploads/                # Uploaded user documents
├── chroma_langchain_db/    # Vector database for document embeddings
├── models/                 # Pre-downloaded models for docling OCR
│   ├── ds4sd--CodeFormula/
│   ├── ds4sd--docling-models/
│   ├── ds4sd--DocumentFigureClassifier/
│   └── EasyOcr/
├── utils/                  # Utility scripts 

📌 Notes

Make sure you have a valid OpenAI API key or any other LLM provider if required.

For large documents, some preprocessing and chunking may be applied automatically.

🙌 Contributing

Feel free to fork this repo, open issues, or submit pull requests. Contributions are welcome!

📄 License

This project is licensed under the Apache 2.0 License – see the LICENSE
 file for details.