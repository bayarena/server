from .models import Motivator
from rest_framework import serializers
from lecture.serializers import LectureSerializer

import io
import os
import PIL
from PIL import Image

from django.core.files.uploadedfile import InMemoryUploadedFile

IMG_SM_SIZE = 60

class MotivatorSerializer(serializers.ModelSerializer):

    lectures = serializers.SerializerMethodField('motivator_lectures')

    def motivator_lectures(self, instance):
        lecs = []
        for lec in instance.lecture_set.all():
            ser = LectureSerializer(lec)
            lecs.append(ser.data)
        return lecs

    class Meta:
        model = Motivator
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

    def create(self, validated_data):

        if validated_data.get('image') is not None:
            return Motivator.objects.create(
                **validated_data,
                image_thumb=self.__resize__(validated_data.get('image'))
                )

        return Motivator.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name_eng = validated_data.get('name_eng', instance.name_eng)
        instance.name_kor = validated_data.get('name_kor', instance.name_kor)
        instance.description = validated_data.get('description', instance.description)

        if validated_data.get('image') is not None:
            instance.image = validated_data.get('image')
            instance.image_thumb = self.__resize__(instance.image)

        instance.save()
        return instance