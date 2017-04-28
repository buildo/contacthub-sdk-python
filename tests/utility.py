from requests import HTTPError


class FakeHTTPResponse:
    def __init__(self, resp_path='tests/util/fake_response', status_code=200):
        self.resp_path = resp_path
        self.status_code = status_code

    @property
    def text(self):
        if not self.resp_path:
            return None
        if self.status_code == 200:
            fake_response = open(self.resp_path, 'r')
            return fake_response.read()
        else:
            http_error_msg = ''
            if self.status_code == 409:
                fake_response = open(self.resp_path, 'r')
                return fake_response.read()

            if 400 <= self.status_code < 500:
                http_error_msg = u'%s Client Error' % self.status_code

            elif 500 <= self.status_code < 600:
                http_error_msg = u'%s Server Error' % self.status_code

            if http_error_msg:
                return '''{
                            "message": "%s",
                            "logref": "06bbabba-fb0f-4b7a-8e5c-0f21fc3e3b39",
                            "data": null,
                            "errors": []
                            }
                        ''' % http_error_msg
