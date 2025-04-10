from flask import Flask, request, jsonify
import pickle
from flask_cors import CORS
import os
import requests
import gdown

app = Flask(__name__)

CORS(app)

FILE_ID = "182LcZMp8lfeDFS6AzzBlTOg81eK8C3EJ"  # Replace with your file ID
MODEL_PATH=gdown.download(f"https://drive.google.com/uc?id={FILE_ID}", "model.pkl", quiet=False)



# Download only once
if not os.path.exists(MODEL_PATH):
    print("Downloading model from Google Drive...")
    response = requests.get(MODEL_URL)
    with open(MODEL_PATH, "wb") as f:
        f.write(response.content)

# Load the model
with open(MODEL_PATH, "rb") as f:
    model, encoders, target_encoder, df = pickle.load(f)
    
@app.route('/predict', methods=["POST"])
def predict():
    data=request.json
    try:
        features=[]
        for col in ["Stream", "Quota", "Category"]:
            features.append(encoders[col].transform([data[col]])[0])
        features.append(float(data["Closing Rank"]))
        feature.append(1)
        
        pred=model.predict_proba([features])[0]
        top_5_colleges=pred.argsort()[-5:][::-1]
        colleges=target_encoder.inverse_transform(top_5_colleges)
        return jsonify({"recommendations": list(colleges)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
if __name__ == "__main__":
    port = 5000
    print(f"Server running at : {port}")
    app.run(port=port)
