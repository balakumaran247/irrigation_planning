import ee
from flask import Flask, jsonify, render_template, request
from src.gee import get_fc, get_ag_area
from src.scenarios import main

# ee.Authenticate()
ee.Initialize()

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/fc/<name>")
def fc(name):
    # Convert the feature collection to GeoJSON
    return jsonify(get_fc(name).getInfo())


@app.route("/image/")
def get_ee_map_url():
    # Define an Earth Engine raster, for instance, a SRTM dataset
    coll = ee.ImageCollection("users/jaltolwelllabs/LULC/IndiaSAT_phase1_draft")
    filtered = coll.filterDate("2021-07-01", "2022-06-30").select(["b1"])
    image = filtered.mosaic()

    # Define visualization parameters in dictionary format
    vis_params = {
        "min": 1,
        "max": 12,
        "palette": [
            "#b2df8a",
            "#6382ff",
            "#d7191c",
            "#f5ff8b",
            "#dcaa68",
            "#33a02c",
            "#50c361",
            "#000000",
            "#dac190",
            "#a6cee3",
            "#38c5f9",
            "#6e0002",
        ],
        "format": "png",
    }

    # Generate tile URL
    map_id = image.getMapId(vis_params)

    return jsonify({"url": map_id["tile_fetcher"].url_format})

@app.route('/area')
def get_area():
    name = request.args.get('name', 'raichur')
    ctype = request.args.get('ctype', 'total')
    return jsonify({'area': f'{round(get_ag_area(ctype, name)/1e4, 2)} ha'})

@app.route('/scenario')
def scenario():
    name = request.args.get('name', 'raichur')
    data = main(name)
    print(data)
    return jsonify(data)
    
if __name__ == "__main__":
    app.run(debug=True)

