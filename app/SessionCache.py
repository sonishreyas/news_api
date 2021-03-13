import time


class SessionCache:

    def __init__(self):
        self.map = dict()

    """
    call to put registers the ip with current time fine grained to seconds. 
    """

    def put(self, ip):
        # time in seconds
        secondsNow = int(time.time())
        self.map.setdefault(ip, []).append(secondsNow)

    def putItems(self, ip, newIntervals):
        self.map[ip] = newIntervals

    """
    get request time mapping to the ip. 
    """

    def get(self, ip):
        if ip in self.map.keys():
            return self.map[ip]
        else:
            return []

    def keys(self):
        return self.map.items()

    def values(self):
        return self.map.values()
