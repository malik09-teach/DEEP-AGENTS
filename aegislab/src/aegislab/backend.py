"""Backend protocol for the sandboxed environment.

This module defines a minimal BackendProtocol class with placeholder
methods for sending and receiving messages. Replace with the actual
implementation as needed.
"""

class BackendProtocol:
    def __init__(self):
        self.connected = False

    def connect(self):
        """Establish a connection to the sandboxed backend."""
        self.connected = True
        # Placeholder: actual connection logic goes here
        return "connected"

    def send(self, message: str):
        """Send a message to the backend.

        Parameters
        ----------
        message: str
            The message payload.
        """
        if not self.connected:
            raise RuntimeError("Backend not connected")
        # Placeholder: send logic
        return f"sent: {message}"

    def receive(self) -> str:
        """Receive a message from the backend.

        Returns
        -------
        str
            Received message.
        """
        if not self.connected:
            raise RuntimeError("Backend not connected")
        # Placeholder: receive logic
        return "placeholder response"
