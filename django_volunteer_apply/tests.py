from django.test import TestCase
from django.urls import reverse
from .models import ActivityManager, Activity, Choice, Person
# Create your tests here.
def create_activities():
    am = ActivityManager.objects.create(name='am')
    a1 = am.activity_set.create(name='a1')
    a2 = am.activity_set.create(name='a2')
    a1.choice_set.create(name='c1')
    a1.choice_set.create(name='c2')
    a2.choice_set.create(name='c3')
    a2.choice_set.create(name='c4')
    p = Person.objects.create(name='p1')

class DetailViewTests(TestCase):
    def test_no_activity_manager(self):
        response = self.client.get(reverse('detail',args=(1,)))
        self.assertEqual(response.status_code, 404)
    def test_activity_post_error(self):
        create_activities()
        response = self.client.post(reverse('detail',args=(1,)), {'data':1})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'does not exist in the database')
        response = self.client.post(reverse('detail',args=(1,)), {'vn':'gao'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'does not exist in the database')

        response = self.client.post(reverse('detail',args=(1,)), {'vn':'p1'})
        self.assertContains(response, 'no # found')

        response = self.client.post(reverse('detail',args=(1,)), {'vn':'p1','id':'1#5'})
        self.assertContains(response, 'nonexistent choice with id')

        response = self.client.post(reverse('detail',args=(1,)), {'vn':'p1','id':'5#1'})
        self.assertContains(response, 'nonexistent activity with id')

        response = self.client.post(reverse('detail',args=(1,)), {'vn':'p1','id':'1#s'})
        self.assertContains(response, 'invalid position_id_text')

        response = self.client.post(reverse('detail',args=(1,)), {'vn':'p1','id':'s#5'})
        self.assertContains(response, 'invalid position_id_text')

        response = self.client.post(reverse('detail',args=(1,)), {'vn':'p1','id':'2#3,2#4'})
        self.assertContains(response, 'you apply two choices for activity. The conflict is')

        response = self.client.post(reverse('detail',args=(1,)), {'vn':'p1','id':'1#2', 'type':'0'})
        self.assertContains(response, 'you cannot cancel a choice')

    def test_activity_success(self):
        create_activities()
        # test successful application
        response = self.client.post(reverse('detail',args=(1,)), {'vn':'p1','id':'1#2,2#3', 'type':'1'})
        self.assertContains(response, 'You apply c2,c3 successfully')
        response = self.client.post(reverse('detail',args=(1,)), {'vn':'p1','id':'1#2,2#3', 'type':'0'})
        self.assertContains(response, 'You cancel c2,c3 successfully')
