# httpcheckd
Presents an HTTP server with results based upon internal server checks.

## Requirments


### Python
- python3.6 or newer
- CherryPy
- dns.resolver
- psutil

### OS
- Linux
- MacOS

May work on Windows, but not tested.

## Usage

### Example

Start with:

```
python3 httpcheckd.py
```

Once running, system checks can be performed by querying URLs. E.g

```
curl 127.0.0.1:8080/resolveDns
```

A successful DNS resolution will return an HTTP 200. A failure will return a 503.

### Supported checks

#### /resolveDns

##### Parameters:

- fqdn (default = google.com)
- dnstype (default = A record)
- nameserver (default = 8.8.8.8)
- timeout (default = 5 seconds)

##### Full paremeter URL example:

/resolveDns?fqdn=amazon.com&dnstype=A&nameserver=1.1.1.1&timeout=3

#### /memUse

##### Parameters:

- percent (default = 95% usage)

##### Full paremeter URL example:

/memUse?percent=90

#### /diskUse

##### Parameters:

- percent (default = 90% usage)
- mount (default = /)

##### Full paremeter URL example:

/diskUse?percent=95&mount=/home

#### /loadAvg

##### Parameters:

- load (default = 4)
- mins (default = 15. Options are 1, 5, 15)

##### Full paremeter URL example:

/loadAvg?load=5&mins=5
