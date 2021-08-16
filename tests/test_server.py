from app.parser import parse_file


def test_parse_file():
    app = parse_file('./tests/server.json')
    assert len(app.urls) == 2

    with open('./tests/server-content.txt') as f:
        assert app.urls[0].content == f.read()
    assert app.urls[1].content == "hello url 2"

    assert app.urls[0].content_type == 'text'
    assert app.urls[0].status == 200
    assert app.urls[0].pattern == '/url/'
    assert len(app.urls[0].headers), 1


def test_build_server_content():
    server = parse_file('./tests/server.json')
    app = server.build()
    client = app.test_client()

    assert client.get('/url/').status_code == 200
    assert client.get('/url/').data == b'some content\n'
    assert next(filter(
        lambda x: x[0] == 'XX', client.get('/url/').headers))[0] == 'XX'

    assert client.get('/url2/').status_code == 200
    assert client.get('/url2/').data == b'hello url 2'


def test_method_list():
    server = parse_file('./tests/server.json')
    app = server.build()
    client = app.test_client()

    assert client.post('/url/').status_code == 405

    assert client.get('/url2/').status_code == 200
    assert client.post('/url2/').status_code == 200
    assert client.get('/url2/').data == b'hello url 2'
    assert client.post('/url2/').data == b'hello url 2'


def test_server_404():
    server = parse_file('./tests/server.json')
    app = server.build()
    client = app.test_client()

    assert client.get('/404/').status_code == 404


def test_same_pattern():
    server = parse_file('./tests/server-same-pattern.json')
    app = server.build()
    client = app.test_client()

    assert len(server.urls) == 1
    assert client.get('/p1/').status_code == 200
    assert client.get('/p1/').data == b'c1'
