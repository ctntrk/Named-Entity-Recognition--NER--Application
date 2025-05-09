from flask import Flask, request, jsonify
from transformers import pipeline, AutoTokenizer
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

model_name = "dslim/bert-base-NER"
tokenizer = AutoTokenizer.from_pretrained(model_name)
ner = pipeline(
    "ner",
    model=model_name,
    tokenizer=tokenizer,
    aggregation_strategy="average"
)

def preprocess_text(text):
    """Metni model için uygun formata getir"""
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'([a-zA-Z])([.!?])', r'\1 \2', text)
    return text

def merge_hyphenated_entities(entities):
    merged = []
    i = 0
    while i < len(entities):
        if i < len(entities)-1 and \
           entities[i]["end"] == entities[i+1]["start"] and \
           entities[i]["entity_group"] == entities[i+1]["entity_group"]:
            
            merged_entity = {
                "entity_group": entities[i]["entity_group"],
                "word": entities[i]["word"] + " " + entities[i+1]["word"],
                "start": entities[i]["start"],
                "end": entities[i+1]["end"],
                "score": (entities[i]["score"] + entities[i+1]["score"])/2
            }
            merged.append(merged_entity)
            i += 2
        else:
            merged.append(entities[i])
            i += 1
    return merged

@app.route("/analyze", methods=["POST"])
def analyze_text():
    data = request.get_json()
    text = data.get("text", "")
    
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        text = preprocess_text(text)
        results = ner(text)
        results = merge_hyphenated_entities(results)
        
        processed = [{
            "entity_group": ent["entity_group"],
            "word": ent["word"],
            "score": float(ent["score"]),
            "start": ent["start"],
            "end": ent["end"]
        } for ent in results]

        return jsonify(processed)
    
    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
