from neomodel import db, clear_neo4j_database
from rest_framework.test import APITestCase

from music_streaming.schema import schema
from music_streaming.models import Song, Album, Musician


class SongTestCase(APITestCase):
    uuid = ""

    def setUp(self):
        clear_neo4j_database(db)

        song = Song(name='testSong').save()

        global uuid
        uuid = song.uuid

        album = Album(name='testAlbum').save()
        song.album.connect(album)

        musicianA = Musician(name='testMusicianA').save()
        musicianB = Musician(name='testMusicianB').save()

        song.musician.connect(musicianA)
        song.musician.connect(musicianB)

    def test_get_album_of_song_should_be_success(self):
        query = """
            query TestQuery($uuid: String!) {
                getAlbumOfSong(uuid: $uuid) {
                    name
                    uuid
                }
            }
        """
        result = schema.execute_sync(
            query,
            variable_values={"uuid": "{}".format(uuid)},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(result.data["getAlbumOfSong"], self.expected_data_get_album_of_song(uuid))

    def expected_data_get_album_of_song(self, uuid):
        song = Song.nodes.get(uuid=uuid)
        album = song.album.get()
        return {"uuid": "{}".format(album.uuid), "name": "{}".format(album.name)}

    def test_get_musicians_of_song_should_be_success(self):
        query = """
            query TestQuery($uuid: String!) {
                getMusiciansOfSong(uuid: $uuid) {
                    name
                    uuid
                }
            }
        """

        result = schema.execute_sync(
            query,
            variable_values={"uuid": "{}".format(uuid)},
        )

        self.assertEqual(result.errors, None)
        self.assertEqual(result.data["getMusiciansOfSong"], self.expected_data_get_musicians_of_song(uuid))

    def expected_data_get_musicians_of_song(self, uuid):
        song = Song.nodes.get(uuid=uuid)
        musicians = song.musician.all()

        musicianList = []
        for m in musicians:
            dataFormat = {"name": "{}".format(m.name), "uuid": "{}".format(m.uuid)}
            musicianList.append(dataFormat)
        return musicianList






class AlbumTestCase(APITestCase):
    pass


class MusicianTestCase(APITestCase):
    pass
