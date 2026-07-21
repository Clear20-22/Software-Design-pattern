"""
OBSERVER PATTERN -- core contracts
-----------------------------------
Observer: anything that wants to react when a Subject changes.
Subject:  anything that maintains a list of Observers and pushes
          updates to them, without knowing what those observers
          actually do with the update (log it, email it, push it
          over a websocket, etc.). This is what keeps the notice
          board decoupled from the notification mechanism.
"""

from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    async def update(self, notice: dict) -> None:
        """Called by the Subject whenever a new notice is published."""
        ...


class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        ...

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        ...

    @abstractmethod
    async def notify(self, notice: dict) -> None:
        ...
