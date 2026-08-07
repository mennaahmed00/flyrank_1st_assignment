**H**yper **T**ext **T**ransfer **P**rotocol **s**ecure --> A **client-server protocol** and an application layer sent over TCP

it is **the foundation of any data exchange on the web.**



HTTP is stateless (every request is independent)



clients and servers communicate by exchanging individual messages

client -send--> messages(requests)

server -send--> message(responses)







user agent = web browser



client   |proxies|(perform different operations)    server(serves the document as requested by the client)



server ---> one server

multiple servers sharing the load (load balancing)





browser(always the entity initiating the request)    |routers, modems, etc.|        server





**proxies numerous functions:**

caching(public or private), filtering(ex. antivirus scan or parental controls), load balancing, authentication(control access to different resources), logging.







**Note:** a connection is controlled at the **transport layer**.

transport protocols on the internet

TCP is reliable but UDP isn't



using http cookies allows you to link requests with the state of the server, this creates session 



servers or clients are often **located on intranets** and hide their true Ip address from other computers.



HTTP requests then go through proxies to cross this network barrier.





**HTTP flow**

client ----wants to communicate with a----> server



1.open a TCP connection(used to send request and receive an answer)

**note:** the client may open a new connection, reuse an existing connection or open several TCP connections to the servers.



2.send an HTTP message, HTTP messages(before HTTP/2) are human readable. with HTTP/2 these messages are encapsulated in frames, and embedded into a binary structure, a frame, allowing optimizations like compression of headers and multiplexing.



3.read the response sent by the server.





4.close or reuse the connection for further requests





**HTTP messages**



requests:

**Get**(method)--> define the operation that client wants to perform  /(path)  HTTP/1.1(protocol version)



Host: developer.mozilla.org

Accept-Language: fr           (Headers)





responses:

HTTP/1.1  200--> status code    ok-->status message







**most commonly used API is fetch API**, can be used to make HTTP requests from JavaScript



server-sent events a one way service that allows a server to send events to the client using HTTP as transport mechanism.



HTTP Methods

Get --> retrieves data from the server

post --> submit data to the server

put -->update data

Delete--> deletes data from the server





set cookie servers send data called cookies to the client

content length 8-bit







**HTTP status code**



1xx: informational    request received/processing

2xx: success          successfully received, understood and accepted

3xx: redirect         further action must be taken

4xx: client error     request doesn't ahve what it needs

5xx: server error     server failed to full an apparent valid request

































