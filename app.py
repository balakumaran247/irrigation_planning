from flask import Flask, render_template,jsonify
import ee

# ee.Authenticate()
ee.Initialize()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fc/')
def fc():
    raichur = ee.FeatureCollection("users/jaltolwelllabs/FeatureCol/Raichur")
    # Convert the feature collection to GeoJSON
    raichur_geoj = jsonify(raichur.getInfo())
    print("JSONIFY Worked")
    return raichur_geoj

@app.route('/image/')
def get_ee_map_url():
    # Define an Earth Engine raster, for instance, a SRTM dataset
    coll = ee.ImageCollection('users/jaltolwelllabs/LULC/IndiaSAT_phase1_draft')
    filtered = coll.filterDate("2021-07-01", "2022-06-30").select(["b1"])
    image = filtered.mosaic()

    # Define visualization parameters in dictionary format
    vis_params = {
        'min': 1,
        'max': 12,
        'palette' : ["#b2df8a","#6382ff","#d7191c","#f5ff8b","#dcaa68","#33a02c","#50c361","#000000","#dac190","#a6cee3","#38c5f9","#6e0002"]
    }

    # Generate tile URL
    map_id = image.getMapId(vis_params)
    print(map_id)

    return jsonify({
        'url': map_id['tile_fetcher'].url_format,
        'mapid': map_id['mapid'],
        'token': map_id['token']
    })

if __name__ == '__main__':
    app.run(debug=True)
