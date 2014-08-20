import messageQueue as MessageQueue


class Scheduler:
    MAX_FRAME_COUNT = 100

    def __init__(self):
        self.messageXOffset = 0
        self.currentFrameCount = 0
        self.messageQueue = MessageQueue()
        return False

    def show_frame(self):
        # puts the image to the LED display
        return False

    def show_message(self):
        # Handles the display of the whole message
        # This includes timing, scrolling, managing offsets

        # uses self.show_frame
        return False

    def poller(self):
        # running / blocking task
        # gets messages from messageQueue
        return False
