#  Drakkar-Software OctoBot-Commons
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


class TentacleRequirements:
    """
    Tree like structure used to keep track of tentacles nested requirements
    """
    def __init__(self, tentacle, config_name):
        self.tentacle = tentacle
        self.tentacle_class = self.tentacle.__class__
        self.config_name = config_name
        self.nested_requirements = []

    def get_requirement(self, tentacle_class, config_name):
        for requirement in self.nested_requirements:
            if requirement.tentacle_class is tentacle_class and requirement.config_name == config_name:
                return requirement
        return None

    def add_requirement(self, requirement):
        if self.get_requirement(requirement.tentacle_class, requirement.config_name) is None:
            self.nested_requirements.append(requirement)

    def get_all_required_tentacles(self, include_self):
        return [req.tentacle for req in self.get_all_nested_requirements(include_self)]

    def get_all_nested_requirements(self, include_self):
        requirements = [self] if include_self else []
        for nested_requirement in self.nested_requirements:
            requirements += nested_requirement.get_all_nested_requirements(True)
        return requirements

    def includes_nested_requirements(self, other):
        for req in other.nested_requirements:
            if req not in self.nested_requirements:
                return False
        return True

    def summary(self):
        """
        Returns a clone of this tentacle requirement with your references to the tentacle instance
        """
        summary_requirement = TentacleRequirements(self.tentacle, self.config_name)
        summary_requirement.tentacle = None
        summary_requirement.nested_requirements = [req.summary() for req in self.nested_requirements]
        return summary_requirement

    def __eq__(self, other):
        return other is not None and \
               self.tentacle_class is other.tentacle_class and \
               self.config_name == other.config_name and \
               self.nested_requirements == other.nested_requirements

    def __str__(self):
        return f"{self.__class__.__name__} with tentacle: {self.tentacle_class.__name__}, " \
               f"config_name: {self.config_name}, " \
               f"{len(self.nested_requirements)} nested_requirements: " \
               f"[{[str(req) for req in self.nested_requirements]}]"
