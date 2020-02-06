##
##      Name:       httpcheckd.py
##
##      Author:     Rory Swann {rory@shirenet.io}
##      
##      Purpose:    Presents an HTTP server with results from an internal server
##                  check. Returns a 200 for a passed check or a 503 for a fail.
##
import cherrypy
import dns.resolver
import psutil

class Dns():
    def __init__(self, fqdn, dnstype, nameservers, timeout):
        ''' Define DNS object '''
        self.fqdn = fqdn
        self.type = dnstype
        self.nameserver = nameservers
        self.timeout = int(timeout)
        self.resolve = dns.resolver.Resolver()
        self.resolve.lifetime = self.timeout
        self.resolve.nameservers = [self.nameserver]

    def doLookup(self):
        ''' Method to perform the DNS lookup '''
        try:
            self.resolve.query(self.fqdn, self.type)
            return True
        except:
            return False

class Ram():
    def __init__(self, percent):
        ''' Define the Ram object '''
        self.percent = int(percent)

    def ramAvailable(self):
        ''' Method to check percent of ram used '''
        f = psutil.virtual_memory()
        if f.percent < int(self.percent):
            return True
        else:
            return False

class Disk():
    def __init__(self, percent, mount):
        ''' Define the Disk object '''
        self.mount = mount
        self.percent = int(percent)

    def diskUsage(self):
        ''' Method to get disk usage as a percentage '''
        d = psutil.disk_usage(self.mount)
        if d.percent < self.percent:
            return True
        else:
            return False

class Load():
    def __init__(self, load, mins):
        ''' Define the Load object '''
        self.load = int(load)
        if mins == "1":
            self.mins = -3
        elif mins == "5":
            self.mins = -2
        elif mins == "15":
            self.mins = -1

    def getLoad(self):
        '''
        Method to get the load average.
        DOESN'T CURRENTLY WORK
        '''
        l = psutil.getloadavg()
        load15 = l[self.mins]  
        if load15 < self.load:
            return True
        else:
            return False

class HttpStart():
    @cherrypy.expose
    def resolveDns(self, fqdn="google.com", dnstype="A", nameserver="8.8.8.8", timeout="5"):
        ''' 
        Expose page to test DNS lookups.
        Defaults to google.com. Can be overridden with /resolveDns?fqdn=example.com
        Full custom example: /resolveDns?fqdn=example.com&nameserver=1.1.1.1&dnstype=A&timeout=5
        '''
        lookup = Dns(fqdn, dnstype, nameserver, timeout)
        if lookup.doLookup():
            return "ok"
        else:
            raise cherrypy.HTTPError(status="503")
    
    @cherrypy.expose
    def memUse(self, percent="95"):
        '''
        Expose page to perform memory usage check.
        Defaults to 95% usage to report failure. Override with /memUse?percent=90
        '''
        mem = Ram(percent)
        if mem.ramAvailable():
            return "ok"
        else:
            raise cherrypy.HTTPError(status="503")

    @cherrypy.expose
    def diskUse(self, percent="90", mount="/"):
        '''
        Expose page to perform disk use check.
        Defaults to 90% usage on '/' to report failure. Override with /diskUse?percent=95
        Full path available /diskUse?percent=95&mount=/
        '''
        disk = Disk(percent, mount)
        if disk.diskUsage():
            return "ok"
        else:
            raise cherrypy.HTTPError(status="503")

    @cherrypy.expose
    def loadAvg(self, load="4", mins="15"):
        '''
        Expose page to check load average.
        Defaults to report failure at value of 4 or above. Override with /loadAvg?load=5
        Full path /loadAvg?load=2&mins=15
        '''
        load = Load(load, mins)
        if load.getLoad():
            return "ok"
        else:
            raise cherrypy.HTTPError(status="503")

def main():
    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': 8080})
    cherrypy.quickstart(HttpStart())

if __name__ == "__main__":
    main()
