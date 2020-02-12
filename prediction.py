from clarifai.rest import Image as ClImage
from clarifai.rest import ClarifaiApp
import sys
import os

def clarifai_predict(link):
    app=ClarifaiApp("a6ab6850952b49f4b31aa72d451a7bff")
    #app = ClarifaiApp("RpBWVHJVCR3g6AZzeITjaNkjZsq7WC0LKQYR9ARF", "MtF-DFcaa2NDzaHBaE0uBtL8NLIhITggwvduQBt8")
    model = app.models.get('My First Application')
    image = ClImage(url=link)

    try:
        print(link)
        print(link)
        print(link)
        print(link)
        print(link)
        print(link)

        the_prediction = model.predict([image])
        return the_prediction
    except:
        print("error occured")
        return None
        return clarifai_predict(link)

def parse_prediction(the_prediction):
    # Debugging prints for investigating Clarifai's data structures:

    # print (the_prediction.keys())
    # print (the_prediction["outputs"])
    # print (type(the_prediction["outputs"]))
    # print (len(the_prediction["outputs"]))
    # print (the_prediction["outputs"][0]["data"]["concepts"])
    # print (the_prediction)
    # print ("")
    # print (the_prediction["outputs"][0]["data"]["concepts"])
    # print (the_prediction["outputs"][0]["data"]["concepts"][0])
    # print (the_prediction["outputs"][0]["data"]["concepts"][0]["id"])
    # print (the_prediction["outputs"][0]["data"]["concepts"][0]["value"])

    predictions = dict()
    for prediction_ in the_prediction["outputs"][0]["data"]["concepts"]:
        predictions[prediction_["id"]] = prediction_["value"]

    def color(val):
        col = {
            0: "#DD0000",
            1: "#DD0000",
            2: "#DD3300",
            3: "#DD3300",
            4: "#AAAA00",
            5: "#00DD00",
            6: "#00DD00",
            7: "#009933",
            8: "#009933",
            9: "#009933",
            10:"#009933"
        }
        return col[int(val*10)]  # lower-rounded int values from 0 to 10

    ordered_predictions = list(reversed(sorted([(val, key, color(val)) for key, val in predictions.items()])))

    return ordered_predictions # list of tuples: [(val, label), (val, label), ...]

    #
    # old dead code under here:
    #

    # following code is for returning in a long tuple of (label, val, label, val, ...) format:
    res = []
    for value, label in top_4_predictions:
        res.append(label)
        res.append(value)

    (result1L, result1, result2L, result2, result3L, result3, result4L, result4) = res
    return (result1L, result1, result2L, result2, result3L, result3, result4L, result4)
