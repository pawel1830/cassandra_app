import json

from django.urls import reverse
from test_project.api.models import Message


class TestMessage(object):
    sample_data1 = {
        "email": "anna.zajkowska@example.com",
        "title": "Interview 3",
        "content": "simple text3",
        "magic_number": 101
    }
    sample_data2 = {
        "email": "jan.kowalski@example.com",
        "title": "Interview 2",
        "content": "simple text 2",
        "magic_number":22
    }
    bad_email_sample_data = {
        "email": "jan.kowalski",
        "title": "Interview 2",
        "content": "simple text 2",
        "magic_number": 22
    }
    sample_data3 = {
        "email": "jan.kowalski@example.com",
        "title": "Interview",
        "content": "simpletext",
        "magic_number": 101
    }

    def test_can_get_message_by_email(self, client):
        Message.objects.create(email=self.sample_data1['email'],
                               title=self.sample_data1['title'],
                               content=self.sample_data1['content'],
                               magic_number=self.sample_data1['magic_number'])
        url = reverse('get-messages', kwargs={'email_value': self.sample_data1['email']})
        response = client.get(url)
        response_data = dict(response.data)
        results = response_data['results'][0]
        assert response.status_code == 200
        assert results['email'] == self.sample_data1['email']
        assert results['title'] == self.sample_data1['title']
        assert results['content'] == self.sample_data1['content']
        assert results['magic_number'] == self.sample_data1['magic_number']

    def test_can_get_message_wrong_email(self, client):
        url = reverse('get-messages', kwargs={'email_value': 'hdjshdsakjd'})
        response = client.get(url)
        assert response.status_code == 400

    def test_can_create_message_correct_data(self, client):
        url = reverse('create-message')

        Message.truncate()
        response = client.post(
            url,
            data=json.dumps(self.sample_data2),
            content_type="application/json"
        )
        message = Message.objects.get(email=self.sample_data2['email'])
        assert response.status_code == 201
        assert message.title == self.sample_data2['title']
        assert message.content == self.sample_data2['content']
        assert message.magic_number == self.sample_data2['magic_number']

    def test_can_create_message_bad_data(self, client):
        url = reverse('create-message')
        response = client.post(
            url,
            data=json.dumps(self.bad_email_sample_data),
            content_type="application/json"
        )
        assert response.status_code == 400

    def test_can_send_messages(self, client):
        url = reverse('send-message')
        magic_number = self.sample_data3['magic_number']
        data = {'magic_number': magic_number}
        Message.objects.create(email=self.sample_data3['email'],
                               title=self.sample_data3['title'],
                               content=self.sample_data3['content'],
                               magic_number=magic_number)
        response = client.post(url, data, content_type="application/json")
        assert Message.objects.filter(magic_number=magic_number).count() == 0
        assert response.status_code == 200

    def test_send_messages_bad_magic_number(self, client):
        url = reverse('send-message')
        data = {'magic_number': 1000}
        response = client.post(url, data, content_type="application/json")
        assert Message.objects.filter(magic_number=1000).count() == 0
        assert response.status_code == 200


