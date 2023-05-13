from rest_framework import serializers
from .models import Xray

class XraySerializer(serializers.ModelSerializer):
    class Meta:
        model = Xray
        fields = '__all__'

        def predict(self):
            data = self.validated_data
            picture = data['picture']
            picture = os.path.join(os.getcwd()+f"/media/chest_image/{chest_pic}")
            modedl_path = r"ml_model/chestExploration.hdf5"
            model = keras.models.load_model(modedl_path)
            gray_image = cv2.imread(chest_pic, 0)
            resized_image = cv2.resize(gray_image, (100, 100))
            scaled_image = resized_image.astype("float32") / 255.0
            sample_batch = scaled_image.reshape(1, 100, 100, 1)  # 1 image, 100, 100 dim , 1 no of chanels
            result = model.predict(sample_batch)
            result[result >= 0.5] = 1  # Normal
            result[result < 0.5] = 0  # Pneimonia
            if result[0][0] == 1:
                result = "Normal"
            else:
                result = "Pneimonia"
            return result