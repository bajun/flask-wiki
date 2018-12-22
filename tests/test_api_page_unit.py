import unittest

from tests.base import Base


class ApiPageTest(Base):
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

    def test_add(self):
        response = self.client.post('/api/page/',
                                    data=self.first_page_original_data)
        self.assertEqual(response.status_code, 200)
        created_page = response.json
        self.assertCountEqual(self.first_page_original_data,
                              {
                                  'title': created_page['title'],
                                  'content': created_page['content']
                              }
                              )

    def test_unique_title(self):
        self.client.post('/api/page/', data=self.first_page_original_data)
        expect_error = self.client.post('/api/page/',
                                        data=self.first_page_original_data)
        self.assertEqual(expect_error.status_code, 500)

    def test_list(self):
        self.client.post('/api/page/', data=self.first_page_original_data)
        self.client.post('/api/page/', data=self.second_page_original_data)

        response = self.client.get('/api/page/',
                                   data=self.first_page_original_data)
        self.assertEqual(len(response.json), 2)

    def test_get_page_by_id(self):
        response = self.client.post('/api/page/',
                                    data=self.first_page_original_data)
        created_page = response.json

        response_get = self.client.get(f'/api/page/{created_page["id"]}/')
        self.assertEqual(response_get.status_code, 200)

        probably_next_page = created_page["id"] + 1
        response_get = self.client.get(f'/api/page/{probably_next_page}/')
        self.assertEqual(response_get.status_code, 500)

    def test_update_page_by_id(self):
        response = self.client.post('/api/page/',
                                    data=self.first_page_original_data)
        created_page = response.json

        response_get = self.client.put(f'/api/page/{created_page["id"]}/',
                                       data=self.new_content)
        self.assertEqual(response_get.status_code, 200)
        self.assertEqual(response_get.json['content'],
                         self.new_content['content'])

        response_put = self.client.put(f'/api/page/{created_page["id"]}/', data={})
        self.assertEqual(response_put.status_code, 500)

        probably_next_page = created_page["id"] + 1
        response_put = self.client.put(f'/api/page/{probably_next_page}/',
                                       data=self.new_content)
        self.assertEqual(response_put.status_code, 500)


if __name__ == "__main__":
    unittest.main()
