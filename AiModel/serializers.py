from rest_framework import serializers
from .models import Xray
from .model_weights import Aimodel
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np
import os

class XraySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Xray
        fields = '__all__'

    def predict(self):
        data = self.validated_data
        picture = data['image']
        picture = os.path.join(os.getcwd()+f"/media/xray_images/{picture}")

        model = Aimodel()
        img = image.load_img(picture, target_size=(384, 384))

        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        pred = model.predict(x)
        result = pred[0][0]

        return str(result)
