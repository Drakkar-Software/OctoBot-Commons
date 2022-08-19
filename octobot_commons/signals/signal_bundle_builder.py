#  Drakkar-Software OctoBot-Trading
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
import octobot_commons.signals.signal_bundle as signal_bundle
import octobot_commons.signals.signal as signal


class SignalBundleBuilder:
    DEFAULT_SIGNAL_CLASS = signal.Signal

    def __init__(self, identifier: str):
        self.signals: list = []
        self.identifier: str = identifier
        self.version: str = None
        self.signal_class = self.__class__.DEFAULT_SIGNAL_CLASS
        self.reset()

    def register_signal(self, topic: str, content: dict, **kwargs):
        self.signals.append(self.create_signal(topic, content, **kwargs))

    def create_signal(self, topic: str, content: dict, **kwargs):
        return self.signal_class(topic, content, **kwargs)

    def is_empty(self) -> bool:
        return not self.signals

    def build(self) -> signal_bundle.SignalBundle:
        return signal_bundle.SignalBundle(
            self.identifier,
            signals=self.signals,
            version=self.version,
        )

    def reset(self):
        self.signals = []
