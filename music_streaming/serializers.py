from rest_framework import serializers


class AlbumSerializer(serializers.BaseSerializer):
    def to_representation(self, album):
        return {
            'name': album.name,
        }
