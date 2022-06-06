import json


async def get_json_from_request(request):

    """ Exctract JSON object from request
    :param request: request from aiohttp
    :return: JSON object
    """

    payload = ''
    stream = request.content
    while not stream.at_eof():
        line = await stream.read()
        payload += line.decode()
    return json.loads(payload)
