from flask import Flask, request, render_template
from PIL import Image, ImageOps
import numpy as np
from keras.models import load_model
import os
app = Flask(__name__,template_folder='templates')
np.set_printoptions(suppress=True)

model = load_model('keras_model.h5', compile=False)

class_names = open('labels.txt', 'r').readlines()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image_file = request.files['image']
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        image = Image.open(image_file).convert('RGB')
        image = image.resize((224, 224), Image.LANCZOS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        reshaped_image_array = normalized_image_array.reshape(1, 224, 224, 3)

        data[0] = reshaped_image_array
        prediction = model.predict(data)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

        #r=os.path.abspath('result.html')
        return render_template('result.html', class_name=class_name, confidence_score=confidence_score)
    else:
        #i=os.path.abspath('index.html')
        return render_template('index.html')
        

if __name__ == '__main__':
    app.run(debug=True)
