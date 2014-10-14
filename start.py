import os
os.system('clear')
import json
import importlib
import argparse
import gevent
import requests
from gevent.threadpool import ThreadPool
from gevent.queue import Queue
from gevent import monkey
monkey.patch_all(thread=False)


input_file = None
threads_count = 0

global_headers = {}
global_post_param = {}
global_query_param = {}
domain = ''
tasks = Queue()


def get_input():
    try:
        global input_file, threads_count
        parser = argparse.ArgumentParser()
        parser.add_argument('--input', help='testcase json file as input')
        parser.add_argument('--threads', help='Thread Pool size (integer)')
        input_file = parser.parse_args().input
        threads_count = int(parser.parse_args().threads)
    except Exception as e:
        print 'Wrong input --help for help : Error(' + str(e) + ')'
        exit(1)
    if input_file is None or threads_count is None:
        print 'Wrong input --help for help'
        exit(1)


def complete_task(test):
    try:
        for i, request in enumerate(test.TEST['request']):
            if 'hooks' in test.TEST:
                test.TEST['request']['hooks'](request)

            if '://' not in request['url']:
                request['url'] = domain + request['url']

            if request.get('headers') is None:
                request['headers'] = {}
            request['headers'].update(test_suite.TEST_ENV['global_headers'])

            if request.get('params') is None:
                request['params'] = {}
            request['params'].update(test_suite.TEST_ENV['global_query_param'])

            if request.get('data') is None:
                request['data'] = {}
            request['data'].update(test_suite.TEST_ENV['global_post_param'])

            print request

            r = requests.Session().request(request['method'], request['url'],
                                           request.get('params'), request.get('data'),
                                           request.get('headers'), request.get('cookies'),
                                           request.get('files'), request.get('auth'),
                                           request.get('timeout'), request.get('allow_redirects', True),
                                           request.get('proxies'), request.get('hooks'),
                                           request.get('stream'), request.get('verify'), request.get('cert'))
            response = test.TEST['response'][i]
            if 'hooks' in response:
                if not response['hooks'](r):
                    return False
            else:
                if 'status_code' in response and r.status_code != response['status_code']:
                    return False
                if 'body' in response and r.content != response['body']:
                    return False
                if 'header' in response:
                    for h in response['headers']:
                        if r.headers.get(h, None) == None:
                            return False
                        elif r.headers[h] != response[h]:
                            return False
    except Exception as e:
        print e
        return False
    return True


def worker():
    while not tasks.empty():
        task = tasks.get()
        test = importlib.import_module(task[:task.find('.py')])
        print '========================================================================'
        print 'Starting Test:', test.TEST['name']
        if complete_task(test) is False:
            print test.TEST['name'], 'Test Failed'
            return

        print test.TEST['name'], 'Test Success'


if __name__ == '__main__':
    get_input()

    test_suite = importlib.import_module(input_file[:input_file.find('.py')])
    print '========================================================================'
    print 'Test Suite Project Name:', test_suite.TEST_ENV['project_name']

    if 'init_hooks' in test_suite.TEST_ENV:
        if not test_suite.TEST_ENV['init_hooks'](global_headers, global_post_param, global_query_param):
            print 'Init Failed'
    domain = '%s://%s' % (test_suite.TEST_ENV['protocol'], test_suite.TEST_ENV['domain'])

    for i in range(0, len(test_suite.TEST_ENV['testcases'])):
        tasks.put_nowait(test_suite.TEST_ENV['testcases'][i])

    pool = ThreadPool(threads_count)
    for _ in range(threads_count):
        pool.spawn(worker)

    pool.join()
