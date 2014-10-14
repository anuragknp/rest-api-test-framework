import requests
def init_handler(global_headers, global_post_param, global_query_param):
    global_headers['X-REST-API'] = 'testing'
    return True


TEST_ENV = {
TEST = {
    'project_name': 'CloudMagic Gamma - Sync APIs',
    'global_headers': {},
    'global_post_param': {},
    'global_query_param': {},
    'init_hooks': init_handler,
    'global_info': {},
    'domain': 'www.example.com',
    'protocol': 'http',
    'testcases': [
        'test1.py',
    ]
}
