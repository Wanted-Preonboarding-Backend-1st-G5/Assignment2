from neomodel               import db, clear_neo4j_database
from rest_framework.test    import APITestCase

from music_streaming.schema import schema
from music_streaming.models import Song, Album, Musician


class SongTestCase(APITestCase):
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
    def setUp(self):
        clear_neo4j_database(db)
        
        self.song1 = Song(name="신나는 노래").save()
        self.song2 = Song(name="즐거운 노래").save()

        self.album1 = Album(name="신나는 앨범").save()
        self.album2 = Album(name="즐거운 앨범").save()
        
        self.musician1 = Musician(name="신난 가수").save()
        self.musician2 = Musician(name="즐거운 가수").save()
        self.musician3 = Musician(name="즐거운 가수 동생").save()

        self.song1.album.connect(self.album1)
        self.song2.album.connect(self.album2)
            
        self.song1.musician.connect(self.musician1)
        self.song2.musician.connect(self.musician2)
        self.song2.musician.connect(self.musician3)

    def tearDown(self):
        clear_neo4j_database(db)

    def test_related_song_of_album(self):
        query = f"""
                query {{
                    getSongOfAlbum(uuid: "{self.album1.uuid}") {{
                        name
                        uuid
                    }}
                }}
                """
        result = schema.execute_sync(query)
        self.assertEqual(result.errors, None)

        expected_data = [self.song1.to_dictionary()]
        self.assertEqual(result.data['getSongOfAlbum'], expected_data)


    def test_related_musician_of_album(self):
        query = f"""
                query {{
                    getMusicianOfAlbum(uuid: "{self.album2.uuid}") {{
                        name
                        uuid
                    }}
                }}
                """
        result = schema.execute_sync(query)
        self.assertEqual(result.errors, None)

        expected_data = [self.musician2.to_dictionary(), self.musician3.to_dictionary()]
        self.assertEqual(result.data['getMusicianOfAlbum'], expected_data)


class MusicianTestCase(APITestCase):
    def setUp(self):
        clear_neo4j_database(db)
        
        self.song1 = Song(name="신나는 노래").save()
        self.song2 = Song(name="즐거운 노래").save()

        self.album1 = Album(name="신나는 앨범").save()
        self.album2 = Album(name="즐거운 앨범").save()
        
        self.musician1 = Musician(name="신난 가수").save()
        self.musician2 = Musician(name="즐거운 가수").save()
        self.musician3 = Musician(name="즐거운 가수 동생").save()

        self.song1.album.connect(self.album1)
        self.song2.album.connect(self.album2)
            
        self.song1.musician.connect(self.musician1)
        self.song2.musician.connect(self.musician2)
        self.song2.musician.connect(self.musician3)


    def tearDown(self):
        clear_neo4j_database(db)


    def test_related_album_of_musician(self):
        query = f"""
                query {{
                    getAlbumOfMusician(uuid: "{self.musician3.uuid}") {{
                        name
                        uuid
                    }}
                }}
                """
        result = schema.execute_sync(query)
        self.assertEqual(result.errors, None)

        expected_data = [self.album2.to_dictionary()]
        self.assertEqual(result.data['getAlbumOfMusician'], expected_data)


    def test_related_song_of_musician(self):
        query = f"""
                query {{
                    getSongOfMusician(uuid: "{self.musician1.uuid}") {{
                        name
                        uuid
                    }}
                }}
                """
        result = schema.execute_sync(query)
        self.assertEqual(result.errors, None)

        expected_data = [self.song1.to_dictionary()]
        self.assertEqual(result.data['getSongOfMusician'], expected_data)