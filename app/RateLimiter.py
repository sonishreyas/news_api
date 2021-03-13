import time

from SessionCache import SessionCache


class RateLimiter:

    def __init__(self, windowDuration=10, maxRequests=10):
        if windowDuration < 1 :
            raise Exception("Window duration cannot be negative.")
        self.windowDuration = windowDuration

        if maxRequests < 1 :
            raise Exception("Max requests cannot be negative.")
        self.maxRequests = maxRequests

        self.sessionCache = SessionCache()
        self.describe()

    def describe(self):
        print(self.sessionCache.keys())
        print(self.sessionCache.values())
        print(self.windowDuration)
        print(self.maxRequests)
    """ abstract rate limit logic and returns false if more than 
        10 requests have been made in last 10 seconds """

    def allow(self, ip):
        secondsNow = int(time.time())

        newIntervals = []
        intervals = self.sessionCache.get(ip)
        for i in intervals:
            if secondsNow - i < self.windowDuration:
                newIntervals.append(i)
        newIntervals.append(secondsNow)
        self.sessionCache.putItems(ip, newIntervals)

        if len(newIntervals) > self.maxRequests:
            return False
        else:
            return True
