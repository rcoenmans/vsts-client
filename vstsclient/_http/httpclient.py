# -----------------------------------------------------------------------------
# The MIT License (MIT)
# Copyright (c) 2018 Robbie Coenmans
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -----------------------------------------------------------------------------

from . import HTTPResponse

class _HTTPClient(object):
    '''
    Takes the request and sends it to cloud service and returns the response.
    '''

    def __init__(self, protocol=None, session=None, timeout=None):
        '''
        :param str protocol:
            http or https.
        :param requests.Session session:
            session object created with requests library (or compatible).
        :param int timeout:
            timeout for the http request, in seconds.
        '''
        self.protocol = protocol
        self.session = session
        self.timeout = timeout

        # By default, requests adds an Accept:*/* and Accept-Encoding to the session, 
        # which causes issues with some Azure REST APIs. Removing these here gives us 
        # the flexibility to add it back on a case by case basis.
        if 'Accept' in self.session.headers:
            del self.session.headers['Accept']

        if 'Accept-Encoding' in self.session.headers:
            del self.session.headers['Accept-Encoding']

        self.proxies = None

    def set_proxy(self, host, port, user, password):
        '''
        Sets the proxy server host and port for the HTTP CONNECT Tunnelling.
        Note that we set the proxies directly on the request later on rather than
        using the session object as requests has a bug where session proxy is ignored
        in favor of environment proxy. So, auth will not work unless it is passed
        directly when making the request as this overrides both.
        :param str host:
            Address of the proxy. Ex: '192.168.0.100'
        :param int port:
            Port of the proxy. Ex: 6000
        :param str user:
            User for proxy authorization.
        :param str password:
            Password for proxy authorization.
        '''
        if user and password:
            proxy_string = '{}:{}@{}:{}'.format(user, password, host, port)
        else:
            proxy_string = '{}:{}'.format(host, port)

        self.proxies = {'http': 'http://{}'.format(proxy_string),
                        'https': 'https://{}'.format(proxy_string)}

    def perform_request(self, request):
        '''
        Sends an HTTPRequest to Azure Storage and returns an HTTPResponse. If 
        the response code indicates an error, raise an HTTPError.    
        
        :param HTTPRequest request:
            The request to serialize and send.
        :return: An HTTPResponse containing the parsed HTTP response.
        :rtype: :class:`~azure.storage.common._http.HTTPResponse`
        '''
        # Construct the URI
        uri = self.protocol.lower() + '://' + request.host + request.path

        # Send the request
        response = self.session.request(request.method,
                                        uri,
                                        params=request.query,
                                        headers=request.headers,
                                        data=request.body or None,
                                        timeout=self.timeout,
                                        proxies=self.proxies)

        # Parse the response
        status = int(response.status_code)
        response_headers = {}
        for key, name in response.headers.items():
            response_headers[key.lower()] = name

        wrap = HTTPResponse(status, response.reason, response_headers, response.content)
        response.close()

        return wrap