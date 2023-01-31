This is a package that can make notifis and overlays in an easy way

### example notification:
```python
from darkdisplay.notification import DisplayNotification

# make an example notification
notification = DisplayNotification(
    message="Hello World!",
    show_button=True,
    button_text="Click Me!",
    window_size="250x150",
    debug=True
)

# auto displays and does not return anything
# to wait until the notification is displayed do this:
from darkdisplay.notification import wait_until_closed

wait_until_closed(notification)

# to get button input you can use this example:
while notification.running:
    if notification.button_function:
        # CODE you want to run
        # at the end reset the button
        notification.button_function = False
    else:
        # sleep to reduce cpu overhead
        sleep(.01)
        pass
```
### example overlay:
```python
from darkdisplay.overlay import Overlay

# make an example overlay
overlay = Overlay(
    message="your text here...",
    window_size="250x85",
    debug=True,
    start_hidden=True
)

# starts overlay
overlay.start()

# shows overlay
overlay.show()

# hide overlay
overlay.hide()

# stop overlay
overlay.close()

# update message/overlay
overlay.update_message(
    message="updated message"
)
```