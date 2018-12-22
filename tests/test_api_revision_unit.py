import random
import unittest

from tests.base import Base


class ApiRevisionTest(Base):
    first_page_original_data = {
        "title": "Title First",
        "content": """Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
            Morbi quis viverra diam. Sed eget leo fermentum, aliquam lacus et, 
            malesuada lorem. Mauris porta dignissim diam, vitae ornare odio 
            laoreet sit amet. Fusce orci eros, consequat et ex vitae, 
            ultricies cursus felis. Nulla dui odio, accumsan et molestie a, 
            fringilla id lorem. Sed at maximus quam. 
            Nulla consectetur magna nunc, at pretium enim sagittis dignissim. 
            Fusce consectetur diam a molestie egestas."""
    }

    second_page_original_data = {
        "title": "Title Second",
        "content": """Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
                Morbi quis viverra diam. Sed eget leo fermentum, aliquam lacus et, 
                malesuada lorem. Mauris porta dignissim diam, vitae ornare odio 
                laoreet sit amet. Fusce orci eros, consequat et ex vitae, 
                ultricies cursus felis. Nulla dui odio, accumsan et molestie a, 
                fringilla id lorem. Sed at maximus quam. 
                Nulla consectetur magna nunc, at pretium enim sagittis dignissim. 
                Fusce consectetur diam a molestie egestas."""
    }

    new_content = {
        "content": """"Nunc nec accumsan felis. 
            Maecenas dignissim a arcu non vestibulum. 
            Nam sollicitudin nibh mauris, molestie rutrum enim vulputate a. 
            Sed ut est et est porttitor aliquam sed vitae augue. 
            Integer facilisis tellus vitae lorem rutrum sollicitudin. 
            Etiam tempus nisi eu lectus interdum, id eleifend diam faucibus. 
            Aliquam sagittis quam ut arcu tempor lacinia. 
            Fusce condimentum cursus ante sed eleifend. 
            Vestibulum sagittis consectetur ex, a tincidunt sapien semper vitae. 
            Donec bibendum nulla suscipit vehicula luctus. 
            Sed et sem ac est vehicula sagittis eu eu felis. 
            Mauris aliquam quis libero vitae congue. 
            Pellentesque habitant morbi tristique senectus et netus et malesuada 
            fames ac turpis egestas. Curabitur eu fermentum nibh."""
    }

    def test_list_revision(self):
        response = self.client.post('/api/page/',
                                    data=self.first_page_original_data)
        created_page = response.json
        self.client.put(f'/api/page/{created_page["id"]}/',
                        data=self.new_content)

        response = self.client.get(
            f"/api/page/{created_page['id']}/revisions/")
        self.assertEqual(len(response.json), 2)

    def test_show_page_by_revision(self):
        response = self.client.post('/api/page/',
                                    data=self.first_page_original_data)
        created_page = response.json
        self.client.put(f'/api/page/{created_page["id"]}/',
                        data=self.new_content)

        response = self.client.get(
            f"/api/page/{created_page['id']}/revisions/")

        random_revision = random.choice(response.json)

        revision_response = self.client.get(
            f"/api/page/{created_page['id']}/revisions/{random_revision['id']}/")

        self.assertEqual(revision_response.status_code, 200)

        probably_next_page = created_page["id"] + 1
        probably_next_revision = random_revision['id'] + 1

        response_error = self.client.get(
            f"/api/page/{probably_next_page}/revisions/{probably_next_revision}/")
        self.assertEqual(response_error.status_code, 500)

    def test_set_revision_as_actual(self):
        response = self.client.post('/api/page/',
                                    data=self.first_page_original_data)
        created_page = response.json
        self.client.put(f'/api/page/{created_page["id"]}/',
                        data=self.new_content)

        response = self.client.get(
            f"/api/page/{created_page['id']}/revisions/")

        random_revision = random.choice(response.json)

        revision_response = self.client.post(
            f"/api/page/{created_page['id']}/revisions/{random_revision['id']}/actual/")

        response = self.client.get(
            f"/api/page/{created_page['id']}/revisions/")

        actual_from_api = [x for x in response.json if x['actual'] == 1]

        self.assertEqual(random_revision['id'], actual_from_api[0]['id'])

        self.assertEqual(revision_response.status_code, 200)

        probably_next_revision = random_revision['id'] + 1
        revision_bad_response = self.client.post(
            f"/api/page/{created_page['id']}/revisions/{probably_next_revision}/actual/")
        self.assertEqual(revision_bad_response.status_code, 500)


if __name__ == "__main__":
    unittest.main()
