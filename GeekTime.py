#!/usr/bin/python

import string
from datetime import datetime

from Foundation import NSObject, NSDate, NSTimer, NSRunLoop, NSDefaultRunLoopMode
from AppKit import NSStatusBar, NSMenu, NSMenuItem, NSApplication
from PyObjCTools import AppHelper


__version__ = '0.1.0'
__author__ = 'Jannis Leidel'


start_time = NSDate.date()


class GeekTime(NSObject):
    statusbar = None
    digs = string.digits + string.lowercase

    def int2base(self, x, base):
        if x < 0:
            sign = -1
        elif x==0:
            return '0'
        else:
            sign = 1
        x *= sign
        digits = []
        while x:
            digits.append(self.digs[x % base])
            x /= base
        if sign < 0:
            digits.append('-')
        digits.reverse()
        return ''.join(digits)

    def updateGeektime(self):
        now = datetime.utcnow()
        year, month, day, hours, minutes, seconds = now.timetuple()[0:6]
        geektime = 65536 * ((3600000 * hours) + (60000 * minutes) + (1000 * seconds) + now.microsecond // 1000) // (24 * 60 * 60 * 1000)
        if (geektime < 1000):
            padding = "0"
        elif (geektime < 100):
            padding = "00"
        elif (geektime < 10):
            padding = "000"
        else:
            padding = ""
        return "0x" + padding + self.int2base(int(geektime), 16).upper()

    def applicationDidFinishLaunching_(self, notification):
        global start_time
        statusbar = NSStatusBar.systemStatusBar()
        # Create the statusbar item
        self.statusitem = statusbar.statusItemWithLength_(70.0)
        # Set initial image
        self.statusitem.setTitle_(self.updateGeektime())
        # Let it highlight upon clicking
        self.statusitem.setHighlightMode_(1)
        
        self.menu = NSMenu.alloc().init()
        menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')
        self.menu.addItem_(menuitem)
        self.statusitem.setMenu_(self.menu)
        
        self.timer = NSTimer.alloc().initWithFireDate_interval_target_selector_userInfo_repeats_(start_time, 0.65, self, 'tick:', None, True)
        NSRunLoop.currentRunLoop().addTimer_forMode_(self.timer, NSDefaultRunLoopMode)
        self.timer.fire()
        
    def tick_(self, notification):
        self.statusitem.setTitle_(self.updateGeektime())
    

def main():
    app = NSApplication.sharedApplication()
    delegate = GeekTime.alloc().init()
    app.setDelegate_(delegate)
    AppHelper.runEventLoop()

if __name__ == "__main__":
    main()
