from flask import make_response


def get_response(data_list):
    response = make_response({"message": data_list[0], "status_code": data_list[1]})
    response.headers['Content-Type'] = 'application/json'
    response.status_code = data_list[1]
    return response


def get_file_content(data):
    response = make_response(data)
    return response


def throw_error(code):
    error_messages = {
        400: "Bad request",
        404: "Not found",
        500: "Internal server error"
    }
    return get_response([error_messages.get(code), code])
