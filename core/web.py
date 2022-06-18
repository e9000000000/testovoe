from flask import Flask, jsonify

from db import Db

app = Flask(__name__)
db = Db()

@app.route("/")
async def get():
    return jsonify([o.serialized for o in await db.get_orders()])


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=80)
