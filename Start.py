import prediction as p
import s3_utils as s3

from flask import Flask, render_template, request, session, send_file, url_for, app, safe_join, send_from_directory
from PIL import Image, ImageOps
import requests
from io import StringIO

import os
import uuid
from collections import OrderedDict


app = Flask(__name__, template_folder='templates')
app.config.from_object(__name__)

app.secret_key = '0yX Rr]A/3TH!j9WX/,?RZmN8j~XHL' # Useful if using sessions. Did not need finally.
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])


@app.route("/")
def hello():
    return render_template('forma.html')

@app.route('/report/<im_uuid>')
def report(im_uuid):
    return render_template(
        'reportgen.html',
        prediction=s3.load_prediction(im_uuid)[0],
        image_link="/imgs/"+im_uuid+".jpg"
    )

@app.route('/result/', methods=['post'])
def result():
    im_uuid = str(uuid.uuid4())

    # Load image from file or url
    link=request.form.get("link", type=str)
    if (link == ""):
        file_u = request.files['file']
        if file_u.filename.split(".")[-1].lower() in ALLOWED_EXTENSIONS:
            img_io = StringIO()
            file_u.save(img_io)
            img_io.seek(0)
            img = Image.open(img_io)
        else:
            pass
            # Maybe return here an error message like "unknown image file extension".
    else:
        img_r = requests.get(link)
        img = Image.open(StringIO(img_r.content))
    # Save image
    new_img_link = s3.add_image(img, im_uuid)

    # Predict on image and save prediction
    the_prediction = p.clarifai_predict(new_img_link)
    prediction_list = p.parse_prediction(the_prediction)
    s3.add_prediction(prediction_list, im_uuid)

    # Cook results
    return render_template(
        'result.html',
        loopdata=prediction_list,
        image_link="/imgs/"+im_uuid+".jpg",
        im_uuid=im_uuid
    )
    # TODO: special yellow coloring for [turbulent fb, coarse bubbling, fine bubble problem, minor turbulence]

# Serving image to user by hiding s3 and resizing:
# See: http://stackoverflow.com/questions/7877282/how-to-send-image-generated-by-pil-to-browser
@app.route('/imgs/<im_uuid>')
def serve_img(im_uuid):
    def serve_pil_image(pil_img):
        img_io = StringIO()
        pil_img.save(img_io, 'JPEG', quality=70)
        img_io.seek(0)
        return send_file(img_io, mimetype='image/jpeg')

    url = s3.bucket_url + im_uuid
    img_r = requests.get(url)
    img = Image.open(StringIO(img_r.content))
    if img.mode != "RGB":
        img = img.convert("RGB")
    # Final resize
    w, h = int(img.size[0]/float(img.size[1])*200), 200
    img = ImageOps.fit(img, (w, h), Image.ANTIALIAS)
    return serve_pil_image(img)


# website_home = "https://imageclasses.herokuapp.com/"
if __name__ == "__main__":
    ##    app.run()
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
