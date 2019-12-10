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

from octobot_commons.event_tree import EventTree


def test_event_tree_init():
    assert EventTree()


@pytest.mark.asyncio
async def test_event_tree_get_new_node():
    event_tree = EventTree()
    created_node = event_tree.get_node(["test"])
    assert event_tree.root.children == {"test": created_node}


@pytest.mark.asyncio
async def test_event_tree_get_existing_node():
    event_tree = EventTree()
    created_node = event_tree.get_node(["test"])
    get_node_result = event_tree.get_node(["test"])
    assert created_node is get_node_result


@pytest.mark.asyncio
async def test_event_tree_set_node():
    event_tree = EventTree()
    created_node = event_tree.get_node(["test"])
    event_tree.set_node(1, None, created_node)
    assert created_node.node_value == 1
    assert created_node.node_type is None


@pytest.mark.asyncio
async def test_event_tree_set_node_at_path():
    event_tree = EventTree()
    event_tree.set_node_at_path("test-string", "test-type", ["test", "test2", "test3"])
    assert event_tree.get_node(["test"])
    assert event_tree.get_node(["test", "test2"])
    assert event_tree.get_node(["test", "test2", "test3"])
    assert event_tree.get_node(["test"]).children
    assert event_tree.get_node(["test", "test2"]).children
    assert not event_tree.get_node(["test", "test2", "test3"]).children
    assert event_tree.get_node(["test", "test2", "test3"]).node_value == "test-string"
    assert event_tree.get_node(["test", "test2", "test3"]).node_type == "test-type"
