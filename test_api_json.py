import pytest

# check json by id
# get positive
@pytest.mark.parametrize("params",
                         [{"var": "1", "result": {'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1}},
                          {"var": "15", "result": {'userId': 1, 'id': 15, 'title': 'ab voluptatum amet voluptas', 'completed': True}}
                          ])
def test_api_positive_response(api_client_brew, params):
    res = api_client_brew.get_brew(
        path="/todos/" + params["var"])
    print(res.json())

    assert res.json() == params["result"]
    assert res.status_code == 200
    assert res.json()["id"] == int(params["var"])


# check get negative
@pytest.mark.parametrize("params",
                         [{"var": "-1", "result": {}},
                          {"var": "0", "result": {}},
                          {"var": "201", "result": {}}
                          ])
def test_api_negative_response(api_client_brew, params):
    res = api_client_brew.get_brew(
        path="/todos/" + params["var"])
    print(res.status_code)

    assert res.status_code == 404
    assert res.json() == params["result"]


# check len in todos,comments
@pytest.mark.parametrize("params",
                         [{"by_som": "/todos", "len": 200},
                          {"by_som": "/comments", "len": 500}
                          ])
def test_api_get_len(api_client_brew, params):
    res = api_client_brew.get_brew(
        path=params["by_som"])

    assert len(res.json()) == params["len"]
    assert res.status_code == 200


# POST REQUESTS
# positive post tests
def test_api_post(api_client_brew):
    post_data = api_client_brew.post_brew(
        path="/todos",
        data={"title": "input_title", "body": "test-test", "userId": "1"})

    assert post_data.status_code == 201
    assert post_data.json()['title'] == "input_title"
    assert post_data.json()['body'] == "test-test"
    assert post_data.json()['userId'] == "1"


# negative post tests - mistakes in path
@pytest.mark.parametrize("path_for_test", ["/ posts", "/post", "/postss"])
def test_api_negative_post(api_client_brew, path_for_test):
    post_data = api_client_brew.post_brew(
        path=path_for_test,
        data={"title": " input_title", "body": "test-test", "userId": 100})
    print(post_data.status_code)

    assert post_data.status_code == 404


def test_exception_post(api_client_brew):
    with pytest.raises(TypeError):
        post_data = api_client_brew.post_brew(
            path="/posts",
            data=[1, 2, 3]
        )


# PUT/PATCH REQUESTS
def test_api_positive_put(api_client_brew):
    put_data = api_client_brew.put_brew(
        path="/todos/13",
        data={"title": "updating title", "body": "test-test-test", "userId": 20})

    print(put_data.status_code, put_data.json)
    assert put_data.status_code == 200
    assert put_data.json()['title'] == "updating title"
    assert put_data.json()['body'] == "test-test-test"
    assert put_data.json()['userId'] == "20"


def test_api_negative_put(api_client_brew):
    put_data = api_client_brew.put_brew(
        path="/todos/0",
        data={"title": "updating title", "body": "test-test-test", "userId": 20})

    print(put_data.status_code, put_data.json)
    assert put_data.status_code == 500


@pytest.mark.parametrize("params",
                         [{"var": "/13", "status": 200},
                          {"var": "/0", "status": 200}
                          ])
def test_api_patch(api_client_brew, params):
    patch_data = api_client_brew.patch_brew(
        path="/todos" + params["var"],
        data={"title": "updating title"})
    print(patch_data.status_code)
    assert patch_data.status_code == params["status"]
    assert patch_data.json()['title'] == "updating title"


# DELETE REQUESTS
@pytest.mark.parametrize("params",
                         [{"var": "/15", "status": 200},
                          {"var": "/150", "status": 200}
                          ])
def test_apt_delete(api_client_brew, params):
    delete_res = api_client_brew.delete_brew(
        path="/todos" + params["var"])
    print(delete_res.status_code)
    assert delete_res.status_code == params["status"]
    assert delete_res.json() == {}


#FILTERING by userID +schema validating
@pytest.mark.parametrize("params",
                         [{"key": "userId", "value": "3", "result": 3},
                          {"key": "completed", "value": "false", "result": False},
                          {"key": "id", "value": "3", "result": 3},
                          {"key": "title", "value": "et doloremque nulla", "result": "et doloremque nulla"}
                          ])
def test_api_positive_filtering(api_client_brew, params):

    res = api_client_brew.get_brew(
        path="/todos?" + params["key"] + "=" + params["value"])

    for i in res.json():
        assert i[params["key"]] == params["result"]



@pytest.mark.parametrize("params",
                         [{"key": "userId", "value": "110", "result": 110},
                          {"key": "completed", "value": "maybe true", "result": False}
                          ])
def test_api_negative_filtering(api_client_brew, params):
    res = api_client_brew.get_brew(
        path="/todos?" + params["key"] + "=" + params["value"])

    assert res.status_code == 200
    assert res.json() == []

