from .models import Lecture
from rest_framework import serializers

import io
import os
import PIL
from PIL import Image

from django.core.files.uploadedfile import InMemoryUploadedFile

IMG_X_SIZE = 400
IMG_Y_SIZE = 300

class LectureSerializer(serializers.ModelSerializer):

    meta_motivator = serializers.SerializerMethodField('motivators_metadata')
    tag = serializers.SerializerMethodField(method_name='category_title')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def motivators_metadata(self, instance):
        meta_motivators = []
        request = None

        if self.context.get("parent_request") :
            request = self.context.get("parent_request")
        else :
            request = self.context['view'].request

        for motivator in instance.motivators.all():
            image_thumb = None
            if motivator.image_thumb :
                image_thumb = request.build_absolute_uri(motivator.image_thumb.url)
            meta_motivators.append({
                'id': motivator.id,
                'name_kor' : motivator.name_kor,
                'image_thumb' : image_thumb
                })
        return meta_motivators

    def category_title(self, instance):
        if instance.category is None :
            return "미분류"
        return instance.category.title

    class Meta:
        model = Lecture
        fields = '__all__'

    def __resize__(self, image):
        img = Image.open(image)

        # Resize and Center crop
        if (img.width / img.height) > (IMG_X_SIZE / IMG_Y_SIZE):
            new_width = int(img.width * IMG_Y_SIZE / img.height)
            new_height = IMG_Y_SIZE
            crop_x1 = int((new_width - IMG_X_SIZE) / 2)
            crop_y1 = 0
            crop_x2 = int((new_width + IMG_X_SIZE) / 2)
            crop_y2 = IMG_Y_SIZE
        else:
            new_width = IMG_X_SIZE
            new_height = int(img.height * IMG_X_SIZE / img.width)
            crop_x1 = 0
            crop_y1 = int((new_height - IMG_Y_SIZE) / 2)
            crop_x2 = IMG_X_SIZE
            crop_y2 = int((new_height + IMG_Y_SIZE) / 2)

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
        instance.date = validated_data.get('date', instance.date)

        instance.category = validated_data.get('category', instance.category)
        instance.description = validated_data.get('description', instance.description)
        instance.theme = validated_data.get('theme', instance.theme)
        instance.difficulty = validated_data.get('difficulty', instance.difficulty)
        instance.time = validated_data.get('time', instance.time)

        instance.staging = validated_data.get('staging', instance.staging)

        instance.motivators.set(validated_data.get('motivators', instance.motivators))

        if validated_data.get('image') is not None:
            instance.image = validated_data.get('image', instance.image)

        instance.main_image = validated_data.get('main_image', instance.main_image)

        instance.save()
        return instance

    def validate_image(self, image):
        if image is not None:
            return self.__resize__(image)