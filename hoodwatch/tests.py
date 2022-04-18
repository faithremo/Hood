from neighbourhoodapp.views import neighbourhood, profile
from django.test import TestCase
from .models import NeighbourHood, Profile, Post, Business


# Create your tests here.
class ProfileTestClass(TestCase):

    def setUp(self):
        self.angela = Profile( name= 'Angela', bio = 'i am a developer', email = 'amutyota@gmail.com', profile_picture= "anfg.jpg", neighbourhood = 'runda hood', location = 'nairobi' )

    def test_instance(self):
        self.assertTrue(isinstance(self.angela, Profile))

    def test_save_method(self):
        self.angela.save_profile()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles) > 0)

class NeighbourhoodTestClass(TestCase):

    def setUp(self):
        self.angela = Profile( name= 'Angela', bio = 'i am a developer', email = 'amutyota@gmail.com', profile_picture= "anfg.jpg", neighbourhood = 'runda hood', location = 'nairobi' )
        self.angela.save_profile()

        self.new_neighbourhood = NeighbourHood(name = 'runda hood', location = 'nairobi', occupants_count= '30', description = 'a nice place', contact = '07156354', health_department = '07156354', police_authorities = '08464')
        self.new_neighbourhood.save()

    def tearDown(self):
        NeighbourHood.objects.all().delete()
        Profile.objects.all().delete()
        Business.objects.all().delete()
        Post.objects.all().delete()

