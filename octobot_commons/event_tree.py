# pylint: disable=R0201
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


class EventTreeNode:
    """
    Node element of a EventTree
    """

    __slots__ = [
        "node_value",
        "node_value_time",
        "node_type",
        "children",
    ]

    def __init__(self, node_value, node_type):
        self.node_value = node_value
        self.node_value_time = None
        self.node_type = node_type
        self.children = {}


class NodeExistsError(Exception):
    """
    Node doesn't exist error
    """


class EventTree:
    """
    Event Tree based on EventTreeNodes
    """

    __slots__ = ["root"]

    def __init__(self):
        """
        Init the root node
        """
        self.root = EventTreeNode(None, None)

    def set_node(self, value, node_type, node, timestamp=0):
        """
        Set the node attributes
        Can raise an exception if the node doesn't exists
        :param value: the node 'node_value' attribute to set
        :param node_type: the node 'node_type' attribute to set
        :param node: the node to update
        :param timestamp: the value modification timestamp.
        """
        self._set_node(node, value, node_type, timestamp=timestamp)

    def set_node_at_path(self, value, node_type, path, timestamp=0):
        """
        Set the node attributes
        Creates the node if it doesn't exists
        :param value: the node 'node_value' attribute to set
        :param node_type: the node 'node_type' attribute to set
        :param path: the node path (as a list of string)
        :param timestamp: the value modification timestamp.
        For example:
        - If you created a first node with the path ["my-parent-node"]
        - You can create a child node of my-parent-node by using ["my-parent-node", "my-new-child-node"] as `path`
        :return: void
        """
        self._set_node(
            self.get_or_create_node(path), value, node_type, timestamp=timestamp
        )

    def get_node(self, path, starting_node=None):
        """
        Get the node at the specified path
        :param path: the node path (as a list of string).
        For example:
        - If you created a first node with the path ["my-parent-node"]
        - You can create a child node of my-parent-node by using ["my-parent-node", "my-new-child-node"] as `path`
        :param starting_node: the node to start the relative path
        :return: the node instance or raise a NodeExistsError if the node doesn't exists
        """
        try:
            return self._get_node(path, starting_node=starting_node)
        except KeyError:
            raise NodeExistsError

    def get_or_create_node(self, path, starting_node=None):
        """
        Get the node at the specified path
        Creates the node if it doesn't exists
        :param path: the node path (as a list of string).
        For example:
        - If you created a first node with the path ["my-parent-node"]
        - You can create a child node of my-parent-node by using ["my-parent-node", "my-new-child-node"] as `path`
        :param starting_node: the node to start the relative path
        :return: the node instance
        """
        try:
            return self._get_node(path, starting_node=starting_node)
        except KeyError:
            return self._create_node_path(path, starting_node=starting_node)

    def _get_node(self, path, starting_node=None):
        """
        Return the node corresponding to the path
        Can raise a KeyError if the path does not exists
        :param path: the path (as a list of string) to the node
        :param starting_node: the node to start the path, root if None
        :return: EventTreeNode at path
        """
        current_node = self.root if starting_node is None else starting_node
        for key in path:
            current_node = current_node.children[key]
        return current_node

    def _create_node_path(self, path, starting_node=None):
        """
        Expensive method that creates the path to the selected node
        :param path: path (as a list of string) to the selected node
        :param starting_node: the node to start the path, root if None
        :return: the created node path
        """
        current_node = self.root if starting_node is None else starting_node
        for key in path:
            try:
                current_node = current_node.children[key]
            except KeyError:
                # create a new node as the current node child
                current_node.children[key] = EventTreeNode(None, None)

                # change to the new node
                current_node = current_node.children[key]

        return current_node

    def _set_node(self, node, value=None, node_type=None, timestamp=0):
        """
        Sets the node attributes
        :param node: the node instance to update
        :param value: the node instance 'node_value' attribute to set (is ignored if None)
        :param node_type: the node instance 'node_type' attribute to set (is ignored if None)
        :param timestamp: the value modification timestamp.
        """
        if value is not None:
            node.node_value = value

        if node_type is not None:
            node.node_type = node_type

        # set the node value modification timestamp
        node.node_value_time = timestamp
