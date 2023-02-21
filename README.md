This is a package that can make notifis and overlays in an easy way

### example notification:
```python
from darkdisplay.notification import DisplayNotification

# make an example notification
DisplayNotification(
    message="Hello World!",
    title_text="Title",
    window_size="250x150",
    window_timeout=5, # time for the window to stay open in seconds
    debug=True
)

# auto displays and does not return anything
# to wait until the notification is done displaying pass wait_until_closed=True, for example:
# make an example notification
DisplayNotification(
    message="Hello World!",
    title_text="Title",
    window_size="250x150",
    debug=True,
    window_timeout=5,
    wait_until_closed=True,
)
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