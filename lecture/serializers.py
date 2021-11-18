from .models import Lecture
from rest_framework import serializers

import io
import os
import PIL
from PIL import Image

from django.core.files.uploadedfile import InMemoryUploadedFile

IMG_SM_SIZE = 150

class LectureSerializer(serializers.ModelSerializer):

    thumbs = serializers.SerializerMethodField('motivator_thumbs')

    def motivator_thumbs(self, instance):
        thumbs = []
        for motivator in instance.motivators.all():
            thumbs.append(motivator.image_thumb.url)
        return thumbs 

    class Meta:
        model = Lecture
        fields = '__all__'

    def __resize__(self, image):
        img = Image.open(image)

        # Resize and Center crop
        if img.width > img.height:
            new_width = int(img.width * IMG_SM_SIZE / img.height)
            new_height = IMG_SM_SIZE
            crop_x1 = int((new_width - IMG_SM_SIZE) / 2)
            crop_y1 = 0
            crop_x2 = int((new_width + IMG_SM_SIZE) / 2)
            crop_y2 = IMG_SM_SIZE
        else:
            new_width = IMG_SM_SIZE
            new_height = int(img.height * IMG_SM_SIZE / img.width)
            crop_x1 = 0
            crop_y1 = int((new_height - IMG_SM_SIZE) / 2)
            crop_x2 = IMG_SM_SIZE
            crop_y2 = int((new_height + IMG_SM_SIZE) / 2)

        img = img.resize((new_width, new_height))
        img = img.crop((crop_x1, crop_y1, crop_x2, crop_y2))       

        # Save data
        img_io = io.BytesIO()
        image_name = image.name.split('.')[0]
        img_format = image.name.split('.')[-1]
        if img_format == 'jpg' :
            img_format = 'jpeg'

        img.save(img_io, format=img_format)
        new_pic = InMemoryUploadedFile(
            img_io,
            None,
            image_name + "_thumb." + img_format,
            'image/' + img_format,
            img.tell,
             None)

        return new_pic

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.subtitle = validated_data.get('subtitle', instance.subtitle)
        instance.date = validated_data.get('date', instance.date)
        instance.motivators.set(validated_data.get('motivators', instance.motivators))

        if validated_data.get('image') is not None:
            instance.image = validated_data.get('image', instance.image)

        instance.save()
        return instance

    def validate_image(self, image):
        if image is not None:
            return self.__resize__(image)