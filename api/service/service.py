import json

class Service():
    def __init__(self, config, service):
        self.config = config

    async def delete_api(self, endpoint):
        #target = self.config.api_url + endpoint
        #session.delete(target)
        pass

    async def put_api(self, endpoint, data):
        #target = self.config.api_url + endpoint
        headers = {'content-type': 'application/json'}
        #session.put(target, json=data, headers=headers)
        pass

    async def post_api(self, endpoint, data):
        #target = self.config.api_url + endpoint
        headers = {'content-type': 'application/json'}
        #session.post(target, json=data, headers=headers)
        pass

    def get_api(self, endpoint):
        #target = self.config.api_url + endpoint
        headers = {'content-type': 'application/json'}
        return dict()
        '''
        try:
            r = session.get(target, headers=headers)
            return json.loads(r._content.decode('utf-8')) 
        except Exception as e:
            print('what?')
            return dict()
        '''


def to_service(config):
    return Service(config)
