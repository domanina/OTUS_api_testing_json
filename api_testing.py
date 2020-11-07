import pytest
import requests
import cerberus
from jsonschema import validate

# check json by id posts
@pytest.mark.parametrize("params",
                         [{"var": "/0", "result": {}},
                          {"var": "/15", "result": {"userId": 2, "id": 15, "title": "eveniet quod temporibus",
                                                    "body": "reprehenderit quos placeat\nvelit minima officia dolores impedit repudiandae molestiae nam\nvoluptas recusandae quis delectus\nofficiis harum fugiat vitae"}},
                          {"var": "/101", "result": {}}
                          ])
def test_api_id_response(api_client_brew, params):
    res = api_client_brew.get_brew(
        path="/posts" + params["var"])

    assert res.json() == params["result"]


# check status posts
@pytest.mark.parametrize("params",
                         [{"var": "/13", "status": 200},
                          {"var": "/15000", "status": 404}
                          ])
def test_api_status_response(api_client_brew, params):
    res = api_client_brew.get_brew(
        path="/posts" + params["var"])
    print(res.status_code)

    assert res.status_code == params["status"]


# check len in users,comments
@pytest.mark.parametrize("params",
                         [{"by_som": "/users", "len": 10},
                          {"by_som": "/comments", "len": 500}
                          ])
def test_api_get_len(api_client_brew, params):
    res = api_client_brew.get_brew(
        path=params["by_som"])

    assert len(res.json()) == params["len"]


# POST REQUESTS
# positive post tests
@pytest.mark.parametrize('input_id, output_id',
                         [(100, '100'),
                          (0, '0')])
@pytest.mark.parametrize('input_title, output_title',
                         [('test', 'test'),
                          ('', ''),
                          (100, '100')])
def test_api_post(api_client_brew, input_id, output_id, input_title, output_title):
    post_data = api_client_brew.post_brew(
        path="/posts",
        data={"title": input_title, "body": "test-test", "userId": input_id})
    print(post_data.status_code, post_data.headers)

    assert post_data.json()['title'] == output_title
    assert post_data.json()['body'] == "test-test"
    assert post_data.json()['userId'] == output_id


# negative post tests - mistakes in path
@pytest.mark.parametrize("path_for_test", ["/ posts", "/post", "/postss"])
def test_api_negative_post(api_client_brew, path_for_test):
    post_data = api_client_brew.post_brew(
        path=path_for_test,
        data={"title": " input_title", "body": "test-test", "userId": 100})
    print(post_data.status_code)

    assert post_data.status_code == 404
    # assert post_data.json()['body'] == "test-test"
    # assert post_data.json()['userId'] == output_id


def test_exception_post(api_client_brew):
    with pytest.raises(TypeError):
        post_data = api_client_brew.post_brew(
            path="/posts",
            data=[1, 2, 3]
        )


# PUT/PATCH REQUESTS
@pytest.mark.parametrize("params",
                         [{"var": "/13", "status": 200},
                          {"var": "/0", "status": 500}
                          ])
def test_api_put(api_client_brew, params):
    put_data = api_client_brew.put_brew(
        path="/posts" + params["var"],
        data={"title": "updating title", "body": "test-test-test", "userId": 20})
    print(put_data.status_code)
    assert put_data.status_code == params["status"]



@pytest.mark.parametrize("params",
                         [{"var": "/13", "status": 200},
                          {"var": "/0", "status": 200}
                          ])
def test_api_patch(api_client_brew, params):
    patch_data = api_client_brew.patch_brew(
        path="/posts" + params["var"],
        data={"title": "updating title"})
    print(patch_data.status_code)
    assert patch_data.status_code == params["status"]

# DELETE REQUESTS
@pytest.mark.parametrize("params",
                         [{"var": "/15", "status": 200},
                          {"var": "/150", "status": 200}
                          ])
def test_apt_delete(api_client_brew, params):
    delete_res = api_client_brew.delete_brew(
        path="/posts" + params["var"])
    print(delete_res.status_code)
    assert delete_res.status_code == params["status"]


#FILTERING by userID +schema validating
@pytest.mark.parametrize("params",
                         [{"var": "3", "status": 200},
                          {"var": "0", "status": 200}
                          ])
def test_api_filtering(api_client_brew, params):
    schema = {
        "type": "object",
        "properties": {
            "id": {"type": "number"},
            "userId": {"type": "number"},
            "title": {"type": "string"},
            "body": {"type": "string"}
        }
    }

    res = api_client_brew.get_brew(
        path="/posts?userId="+params["var"])
    print(type(res.json()))
    print(res.json())



    assert res.status_code == params["status"]
    for i in res.json():
        validate(instance=i, schema=schema)


