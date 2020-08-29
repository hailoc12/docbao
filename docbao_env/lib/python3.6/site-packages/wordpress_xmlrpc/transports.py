from wordpress_xmlrpc.compat import xmlrpc_client, http_client


class ProxiedTransport(xmlrpc_client.Transport):
    def set_proxy(self, proxy):
        self.proxy = proxy

    def make_connection(self, host):
        self.host = host
        return http_client.HTTP(self.proxy)

    def send_request(self, connection, handler, request_body):
        connection.putrequest("POST", "http://%s%s" % (self.host, handler))

    def send_host(self, connection, host):
        connection.putheader('Host', host)
