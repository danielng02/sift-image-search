from queries import knnQuery, rangeQuery, json_to_df
from database import truncateOrCreateDB, save_items_to_db
from image_processing import process_image_directory, match_images

from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)


@app.route('/image/<path:directory>/<path:filename>')
def image_display(directory, filename):
    return send_from_directory(directory, filename)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/load', methods=['POST'])
def load_directories():
    try:
        matches_db = truncateOrCreateDB('matches_db.json')

        data = request.get_json()

        processed_img1 = process_image_directory(data["path1"])

        processed_img2 = process_image_directory(data["path2"])

        if not processed_img1 or not processed_img2:
            return jsonify(message="No images found"), 400

        matches = match_images(processed_img1, processed_img2)
        save_items_to_db(matches_db, matches)
        matches = match_images(processed_img2, processed_img1)
        save_items_to_db(matches_db, matches)

        return jsonify(message="Images processed and saved successfully"), 200
    except Exception as e:
        return jsonify(message=str(e)), 500

@app.route('/visualise', methods=['POST', 'GET'])
def visualise():
    try:
        if request.args.get('rangeEnabled') == 'true':
            queryResult = rangeQuery(int(request.args.get('range')))
        elif request.args.get('rangeEnabled') == 'false':
            queryResult = knnQuery(int(request.args.get('kNN')))
        else:
            raise Exception("No query type selected")

        df = json_to_df(queryResult)
        records = df.to_dict('records')
        return render_template('visualisation.html', records=records)

    except Exception as e:
        return jsonify(message=str(e)), 500


if __name__ == '__main__':
    app.run(port=8000, debug=True)
