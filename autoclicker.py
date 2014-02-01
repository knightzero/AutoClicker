import wx
import win32api
import win32con #for the VK keycodes
from threading import *
import time
EVT_RESULT_ID = wx.NewId()

def mouseClick():
    print "Click!"
    x,y = win32api.GetCursorPos()
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0) 
    time.sleep(0.05) 
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0) 

def EVT_RESULT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_RESULT_ID, func)
    
class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data
        
class WorkerThread(Thread):
    '''Worker Thread Class.'''
    def __init__(self, notify_window, timer):
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = False
        self.timer = timer
        self.start()
        
    def run(self):
        while True:
            if self._want_abort:
                wx.PostEvent(self._notify_window, ResultEvent(None))
                return
            mouseClick()
            print self.timer
            time.sleep(self.timer)
        
    def abort(self):
        self._want_abort = True


class Frame1(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        
        self.autoClick = False
        self.worker = None
        self.__set_properties()
        self.regHotKey()
        self.Bind(wx.EVT_HOTKEY, self.handleHotKey, id=self.hotKeyId)
        self.slider1 = wx.Slider(self, -1, 1, 1, 10000, (10, 10), (300, 50),
            wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)
    def __set_properties(self):
        self.SetTitle("AutoClicker")
        self.SetSize((300, 100))
        self.SetBackgroundColour("white")
        
    def regHotKey(self):
        """
        This function registers the hotkey Alt+F1 with id=100
        """
        self.hotKeyId = 100
        self.RegisterHotKey(
            self.hotKeyId, #a unique ID for this hotkey
            win32con.MOD_ALT, #the modifier key
            win32con.VK_F1) #the key to watch for
    def handleHotKey(self, evt):
        """
        Prints a simple message when a hotkey event is received.
        """
        self.autoClick = not self.autoClick
        if self.autoClick:
            self.worker = WorkerThread(self, float(1/float(self.slider1.GetValue())))
        else:
            self.worker.abort()
            self.worker = None
        print self.autoClick

class AutoClicker(wx.App):
    def OnInit(self):
        frame1 = Frame1(None, wx.ID_ANY, "")
        self.SetTopWindow(frame1)
        frame1.Show()
        return 1

autoClicker = AutoClicker(0)
autoClicker.MainLoop()