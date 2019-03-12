import webtest

import hello281


def test_get():
    app = webtest.TestApp(hello281.app)

    response = app.get('/')

    assert response.status_int == 200
    assert response.body == 'Hello, welcome to my homepage for CMPE202 lab2!'
