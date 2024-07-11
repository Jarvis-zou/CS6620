from flask import Flask, request, jsonify

app = Flask(__name__)
data_store = {}

@app.route('/items/<string:item_id>', methods=['GET'])
def get_item(item_id):
    item = data_store.get(item_id)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

@app.route('/items', methods=['POST'])
def create_item():
    item_id = request.json.get('id')
    data_store[item_id] = request.json
    return jsonify({"message": "Item created"}), 201

@app.route('/items/<string:item_id>', methods=['PUT'])
def update_item(item_id):
    if item_id in data_store:
        data_store[item_id].update(request.json)
        return jsonify({"message": "Item updated"}), 200
    return jsonify({"error": "Item not found"}), 404

@app.route('/items/<string:item_id>', methods=['DELETE'])
def delete_item(item_id):
    if item_id in data_store:
        del data_store[item_id]
        return jsonify({"message": "Item deleted"}), 200
    return jsonify({"error": "Item not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)