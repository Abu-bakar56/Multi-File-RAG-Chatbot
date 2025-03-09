# Multi-File RAG ChatBot 🤖

An advanced **Retrieval-Augmented Generation (RAG)** chatbot that supports multi-file document processing, enabling intelligent responses based on the uploaded content. Built with **LangChain**, **Google Generative AI (Gemini 1.5 Flash)**, and **Gradio** for an intuitive user experience.

---

## 🔹 Features ✨

✔ **Multi-file document support** (PDFs, TXTs, DOCXs, etc.)  
✔ **Retrieval-Augmented Generation (RAG)** for context-aware responses  
✔ **Google Generative AI (Gemini 1.5 Flash)** for intelligent conversations  
✔ **Gradio-based UI** for easy interaction  
✔ **Secure API key management** using environment variables  
✔ **Efficient, scalable, and easy to deploy**  

---

## 🛠 Installation & Setup 🚀

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/your-username/multi-file-rag-chatbot.git
cd multi-file-rag-chatbot
```

### 2️⃣ Set Up Virtual Environment (Optional)
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Configure API Key 🔑
#### Option 1: Local Setup (For Development)
Create a `.env` file in the project directory and add your API key:
```
GOOGLE_API_KEY=your_api_key_here
```

#### Option 2: GitHub Actions (For Deployment)
1. Go to **GitHub Repository → Settings → Secrets and Variables → Actions**.
2. Click **New Repository Secret**.
3. Name it **GOOGLE_API_KEY** and paste your API key.

---

## 🚀 Usage

Run the chatbot with:
```sh
python app.py
```
Then, open **http://127.0.0.1:7862/** in your browser and start chatting with your documents!

---

## 🎨 Preview
![Chatbot UI Preview](preview-image.png)  

---

## 🔗 Live Demo 🌐
🚀 Try it out here: **[Live Demo](https://your-live-demo-link.com)**

---

## 📜 License
© 2024 **AbuBakar Shahzad** | All Rights Reserved

