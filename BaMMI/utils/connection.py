import requests


def handle_request(request):
    try:
        request.raise_for_status()
        return request
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Something, somewhere went terribly wrong: {e}")


def get_from_url(url: str, headers: dict = "") -> requests.Response:
    """
    Sends a get request to the provided url adding the passed headers and params.
    """
    data_request = requests.get(url, headers=headers)
    return handle_request(data_request)


def post_from_url(url: str, headers: dict = "", data="", files="", params: dict = "") -> requests.Response:
    """
    Sends a post request to the provided url adding the passed headers, data, files and params.
    """
    data_request = requests.post(url, headers=headers, data=data, files=files, params=params)
    return handle_request(data_request)
