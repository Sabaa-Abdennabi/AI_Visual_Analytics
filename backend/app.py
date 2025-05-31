from flask import Flask, request, jsonify
from backend.pipeline import run_pipeline  
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)  # This will allow all origins by default
@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No JSON payload provided'}), 400
    url = data.get('url')
    if not url:
        return jsonify({'error': 'Missing url'}), 400
    # Call pipeline function
    metrics=run_pipeline(url)
    heatmap_path = f"../smooth_heatmap.png"
    return jsonify(metrics), 200, {'X-Heatmap-Path': heatmap_path}
    #mazel appel l LLM

if __name__ == '__main__':
    app.run(debug=True)
