def handler(response):
    print 'handler'
    TEST['request'][1]['url'] = '/xyz/fdsa'
    return True


#<request>
'''self, method, url,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None'''


TEST = {
        'name': 'Sample Test 1',
        'request': [
        {
                'method': 'GET',
                'url': '/sample/get1',
                #'params': {'key': 'value'},
                #'data': {'key': 'value'},
                'timeout': 60,
               # 'headers': {'key': 'value'}
        },
        {
                'method': 'GET',
                'url': '/sample/get2',
                #'params': {'key': 'value'},
                #'data': {'key': 'value'},
                'timeout': 60,
               # 'headers': {'key': 'value'}
        }
        ],
        'response': [
        {
                'http_status': 411,
                #'body': 'result',
                #'header': {'key': 'value'},
                'hooks': handler
        },
        {
                'http_status': 411,
                #'body': 'result',
                #'header': {'key': 'value'}
        }
        ]
}



