# 📄 Named Entity Recognition (NER) Application

This project is a Named Entity Recognition (NER) application that identifies entities such as people, organizations, locations, and miscellaneous types from any given text. It provides an interactive and user-friendly web interface backed by a powerful BERT model and a simple REST API.

---

## 🚀 Features

* 👤 Detects **People**, 🏢 **Organizations**, 🌍 **Locations**, and 📌 **Miscellaneous** entities
* 🎨 Intuitive, color-coded result visualization with icons
* 📊 Displays confidence scores for each entity
* 🔁 Merges hyphenated or multi-word entities
* 📋 Groups results by entity category for clarity

---

## 🧠 About the Application

The project consists of two main components:

1. **Flask API (Backend)**

   * Processes incoming text
   * Uses a BERT-based model to identify named entities
   * Merges adjacent, related tokens and returns the result as JSON

2. **Streamlit Interface (Frontend)**

   * Accepts user input via web UI
   * Sends the text to the backend for analysis
   * Visualizes results with grouped statistics and detailed views

---

## 🖥️ Technology Stack

| Component      | Technology                           |
| -------------- | ------------------------------------ |
| AI Model       | `dslim/bert-base-NER` (Hugging Face) |
| Backend        | Flask REST API                       |
| Frontend       | Streamlit                            |
| NLP Processing | Transformers, Tokenizer              |
| Others         | requests, torch, flask-cors          |

---

## ⚙️ Setup Instructions

1. Install the required libraries:

```bash
pip install -r requirements.txt
```

2. Start the Flask API:

```bash
python backend_app.py
```

3. Run the Streamlit frontend:

```bash
streamlit run ner_app.py
```

---

## 📌 How to Use

1. ✍️ Type or paste text into the input box
2. 🔍 Click the **Analyze** button
3. 📊 Results will appear grouped by entity type and include confidence levels
4. 🧹 Click **Clear** to reset the input field

---

## ✅ Code Overview

* `reset_form()`: Clears input and previous analysis results in the UI
* `preprocess_text()`: Cleans and formats text for model input
* `merge_hyphenated_entities()`: Merges related adjacent words into one entity
* `analyze_text()`: Flask route that processes the text, runs inference, and returns a structured result
* Frontend: Handles button events, calls the API, and renders styled output with HTML & CSS

---

## ⚠️ Known Limitations

* Best performance on texts up to \~500 characters
* May have lower confidence on rare or ambiguous entity types
* Model is context-sensitive and may misclassify in some edge cases


## 📈 Conclusion

This application simplifies the complex task of Named Entity Recognition by combining a powerful transformer model with an easy-to-use web interface. It accurately identifies and categorizes entities in natural language text. The clean code structure and modular components make it a solid foundation for educational purposes, further research, or real-world NLP projects.

---

## 📝 License

This project is licensed under the **MIT License**.
You are free to use, modify, and distribute this software as long as the original license and copyright
notice are included in all copies or substantial portions of the software.

> For full details, see the [LICENSE](LICENSE) file in the project root.
