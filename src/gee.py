import ee
ee.Initialize()

def get_fc(name):
    if name == 'raichur':
        return ee.FeatureCollection("users/jaltolwelllabs/FeatureCol/Raichur")
    elif name == 'raichurCCA':
        return ee.FeatureCollection("users/jaltolwelllabs/FeatureCol/Raichur_Scenario_1_CCA")
    else:
        return None

def get_image():
    coll = ee.ImageCollection("users/jaltolwelllabs/LULC/IndiaSAT_phase1_draft")
    filtered = coll.filterDate("2021-07-01", "2022-06-30").select(["b1"])
    return filtered.mosaic()

def get_ag_area(ctype, name):
    roi = get_fc(name)
    if not roi:
        return None
    image = get_image()
    crop_px_list = [5,9,10,11,12]
    single_px_list = [9, 10]
    double_px = 11
    triple_px = 12
    def extract_px(image, px_list):
        mask = image.eq(px_list[0])
        for i in px_list[1:]:
            mask = mask.Or(image.eq(i))
        return mask
    def get_area(image):
        area_image = image.multiply(ee.Image.pixelArea())
        area = area_image.reduceRegion(
                    reducer=ee.Reducer.sum(),
                    geometry=roi,
                    scale=30,
                    maxPixels=1e12
                )
        return area.get('b1').getInfo()
    # extract the pixels into a binary image
    crop_image = extract_px(image, crop_px_list)
    single_image = extract_px(image, single_px_list)
    double_image = image.eq(double_px)
    triple_image = image.eq(triple_px)
    single = get_area(single_image)
    double = get_area(double_image)
    triple = get_area(triple_image)
    total = get_area(crop_image)
    if ctype == 'single':
        return single
    elif ctype == 'double':
        return double
    elif ctype == 'triple':
        return triple
    elif ctype == 'total':
        return total
    elif ctype == 'kharif':
        return (single+double)
    elif ctype == 'rabi':
        return double
    else:
        return None
