import datetime as dt
import struct


class Thought:

    def __init__(self, user_id, timestamp, thought):
        self.user_id = user_id
        self.timestamp = timestamp
        self.thought = thought

    def __repr__(self):
        return f"Thought(user_id={self.user_id!r}, timestamp={self.timestamp!r}, thought={self.thought!r})"

    def __str__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] user {self.user_id}: {self.thought}"

    def __eq__(self, other):
        if not isinstance(other, Thought):
            return False
        if self.user_id != other.user_id or self.timestamp != other.timestamp or self.thought != other.thought:
            return False
        return True

    def serialize(self):
        thought_in_bytes = self.thought.encode("utf-8")
        return struct.pack('<QQL{}s'.format(len(thought_in_bytes)), self.user_id, int(self.timestamp.timestamp()),
                           len(thought_in_bytes), thought_in_bytes)

    @classmethod
    def deserialize(cls, data):
        user_id, timestamp, thought_size = struct.unpack('<QQL', data[:20])
        thought = struct.unpack('<{}s'.format(thought_size), data[20:])[0].decode("utf-8")
        timestamp_datetime_format = dt.datetime.fromtimestamp(timestamp)
        return cls(user_id, timestamp_datetime_format, thought)
