from flask import Flask, request, jsonify
from pipeline import run_pipeline  
app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No JSON payload provided'}), 400
    url = data.get('url')
    if not url:
        return jsonify({'error': 'Missing url'}), 400
    # Call pipeline function
    run_pipeline(url)
    heatmap_path = f"heatmap/smooth_heatmap.png"
    #mazel appel l LLM

if __name__ == '__main__':
    app.run(debug=True)
