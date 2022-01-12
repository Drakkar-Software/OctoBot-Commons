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
import pytest

from octobot_commons.event_tree import EventTree, NodeExistsError


def test_event_tree_init():
    assert EventTree()


def test_event_tree_get_new_node():
    event_tree = EventTree()
    created_node = event_tree.get_or_create_node(["test"])
    assert event_tree.root.children == {"test": created_node}


def test_event_tree_get_existing_node():
    event_tree = EventTree()
    created_node = event_tree.get_or_create_node(["test"])
    get_node_result = event_tree.get_or_create_node(["test"])
    assert created_node is get_node_result


def test_event_tree_get_not_existing_node():
    event_tree = EventTree()
    with pytest.raises(NodeExistsError):
        assert event_tree.get_node(["test"]) is None


def test_event_tree_delete_existing_node():
    event_tree = EventTree()
    created_node = event_tree.get_or_create_node(["test"])
    delete_node_result = event_tree.delete_node(["test"])
    assert created_node is delete_node_result
    with pytest.raises(NodeExistsError):
        event_tree.get_node(["test"])


def test_event_tree_delete_not_existing_node():
    event_tree = EventTree()
    with pytest.raises(NodeExistsError):
        event_tree.delete_node(["test"])


def test_event_tree_get_new_relative_node():
    event_tree = EventTree()
    created_node = event_tree.get_or_create_node(["test"])
    relative_created_node = event_tree.get_or_create_node(["test-relative"], starting_node=created_node)
    get_node_result = event_tree.get_or_create_node(["test", "test-relative"])
    assert relative_created_node is get_node_result


def test_event_tree_get_relative_node():
    event_tree = EventTree()
    created_node = event_tree.get_or_create_node(["test"])
    relative_created_node = event_tree.get_or_create_node(["test", "test-relative"])
    get_node_result = event_tree.get_or_create_node(["test-relative"], starting_node=created_node)
    assert relative_created_node is get_node_result


def test_event_tree_delete_relative_node():
    event_tree = EventTree()
    created_node = event_tree.get_or_create_node(["test"])
    relative_created_node = event_tree.get_or_create_node(["test", "test-relative"])
    delete_node_result = event_tree.delete_node(["test-relative"], starting_node=created_node)
    assert relative_created_node is delete_node_result
    assert event_tree.get_node(["test"]) is created_node
    with pytest.raises(NodeExistsError):
        event_tree.get_node(["test", "test-relative"])


def test_event_tree_set_node():
    event_tree = EventTree()
    created_node = event_tree.get_or_create_node(["test"])
    event_tree.set_node(1, None, created_node)
    assert created_node.node_value == 1
    assert created_node.node_type is None
    event_tree.set_node(5, None, created_node, timestamp=10)
    assert created_node.node_value == 5
    assert created_node.node_type is None
    assert created_node.node_value_time == 10


def test_event_tree_set_node_at_path():
    event_tree = EventTree()
    event_tree.set_node_at_path("test-string", "test-type", ["test", "test2", "test3"])
    assert event_tree.get_or_create_node(["test"])
    assert event_tree.get_or_create_node(["test", "test2"])
    assert event_tree.get_or_create_node(["test", "test2", "test3"])
    assert event_tree.get_or_create_node(["test"]).children
    assert event_tree.get_or_create_node(["test", "test2"]).children
    assert not event_tree.get_or_create_node(["test", "test2", "test3"]).children
    assert event_tree.get_or_create_node(["test", "test2", "test3"]).node_value == "test-string"
    assert event_tree.get_or_create_node(["test", "test2", "test3"]).node_type == "test-type"
