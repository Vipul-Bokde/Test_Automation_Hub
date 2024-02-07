import time

# ---------------
# Switch Between Tabs
# ---------------

def switch_to_child_window(self):
    time.sleep(0.5)
    #get current window handle
    parent_window_handle = self.driver.current_window_handle
    #get multiple child windows
    child_windows = self.driver.window_handles
    for window in child_windows:
	    #If Parent window id not equal to child one
        if(window!= parent_window_handle):
            # switch to child window
            self.driver.switch_to.window(window)
            break

