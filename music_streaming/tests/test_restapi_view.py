from rest_framework      import status
from rest_framework.test import APITestCase

from neomodel import db, clear_neo4j_database

from music_streaming.models import Song, Album, Musician


class TestCase(APITestCase):
    pass

class SongViewTest(APITestCase):
    clear_neo4j_database(db)

    def setUp(self):
        clear_neo4j_database(db)
        self.song1 = Song(name="커피노래").save()
        self.song2 = Song(name="우유노래").save()

        self.album1 = Album(name="커피앨범").save()
        self.album2 = Album(name="우유앨범").save()
        
        self.musician1 = Musician(name="커피뮤지션").save()
        self.musician2 = Musician(name="우유뮤지션").save()

        self.song1.album.connect(self.album1)
        self.song2.album.connect(self.album2)
            
        self.song1.musician.connect(self.musician1)
        self.song2.musician.connect(self.musician2)
    
    # def tearDown(self):
    #     clear_neo4j_database(db)

    def test_create_success(self):
        data = {
            'name'     : "생성한노래"
        }
        
        response = self.client.post('/songs/', data=data)
        expected_data = {
            "song": "생성한노래"
        }
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.json(), expected_data)

    def test_create_fail(self):
        data = {
            ''     : "",
        }
        response = self.client.post('/songs/', data=data)
        
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'error':'name field is required.'})

    def test_get_list_success(self):
        response = self.client.get('/songs/')
        expected_data = [{
            "song": "커피노래"
        },
        {
            "song": "우유노래"
        }]
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.json(), expected_data)
    
    def test_get_one_list_success(self):
        response = self.client.get(f'/songs/{self.song1.uuid}/')
        expected_data = {
            "name": "커피노래"
        }
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_data)

    def test_get_one_list_fail(self):
        response = self.client.get(f'/songs/{self.song1.uuid[:-1]}/')
        expected_data = {
            "name": "커피노래"
        }
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'error': 'DoesNotExist'})

    def delete_success(self):
        response = self.client.get(f'/songs/{self.song1.uuid}/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_album_of_song_success(self):
        response = self.client.get(f'/songs/{self.song1.uuid}/album/')
        expected_data = [{
            "name": "커피앨범"
        }]
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_data)
    
    def test_album_of_song_fail(self):
        response = self.client.get(f'/songs/{self.song1.uuid[:-1]}/album/')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'error': 'DoesNotExist'})

    def test_musicians_of_song_success(self):
        response = self.client.get(f'/songs/{self.song1.uuid}/musicians/')
        expected_data = [{
            "name": "커피뮤지션"
        }]
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_data)
    
    def test_musician_of_song_fail(self):
        response = self.client.get(f'/songs/{self.song1.uuid[:-1]}/musicians/')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'error': 'DoesNotExist'})

