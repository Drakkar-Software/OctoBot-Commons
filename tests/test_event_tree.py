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
import asyncio
from unittest.mock import patch

import pytest

from octobot_commons.event_tree import EventTree


async def async_event_tree_set_node(tree, value, node_type, node):
    tree.set_node(value, node_type, node)


def test_event_tree_init():
    assert EventTree()


@pytest.mark.asyncio
async def test_event_tree_get_new_node():
    event_tree = EventTree()
    created_node = event_tree.get_or_create_node(["test"])
    assert event_tree.root.children == {"test": created_node}


@pytest.mark.asyncio
async def test_event_tree_get_existing_node():
    event_tree = EventTree()
    created_node = event_tree.get_or_create_node(["test"])
    get_node_result = event_tree.get_or_create_node(["test"])
    assert created_node is get_node_result


@pytest.mark.asyncio
async def test_event_tree_get_new_relative_node():
    event_tree = EventTree()
    created_node = event_tree.get_or_create_node(["test"])
    relative_created_node = event_tree.get_or_create_node(["test-relative"], starting_node=created_node)
    get_node_result = event_tree.get_or_create_node(["test", "test-relative"])
    assert relative_created_node is get_node_result


@pytest.mark.asyncio
async def test_event_tree_get_relative_node():
    event_tree = EventTree()
    created_node = event_tree.get_or_create_node(["test"])
    relative_created_node = event_tree.get_or_create_node(["test", "test-relative"])
    get_node_result = event_tree.get_or_create_node(["test-relative"], starting_node=created_node)
    assert relative_created_node is get_node_result

@pytest.mark.asyncio
async def test_event_tree_set_node():
    event_tree = EventTree()
    created_node = event_tree.get_or_create_node(["test"])
    event_tree.set_node(1, None, created_node)
    assert created_node.node_value == 1
    assert created_node.node_type is None


@pytest.mark.asyncio
async def test_event_tree_set_node_at_path():
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


@pytest.mark.asyncio
async def test_event_tree_set_node_event():
    event_tree = EventTree()
    created_node = event_tree.get_or_create_node(["test"])
    with patch('asyncio.Event.set') as event_set:
        event_tree.set_node(2, None, created_node)
        event_set.assert_called_once()


@pytest.mark.asyncio
async def test_event_tree_clear_node_event():
    event_tree = EventTree()
    created_node = event_tree.get_or_create_node(["test"])
    with patch('asyncio.Event.clear') as event_clear:
        event_tree.set_node(2, None, created_node)
        asyncio.get_event_loop().call_soon(event_clear.assert_called_once)


@pytest.mark.asyncio
async def test_event_tree_parent_node_event():
    event_tree = EventTree()
    created_node = event_tree.get_or_create_node(["test"])
    await asyncio.gather(*[async_event_tree_set_node(event_tree, 2, None, created_node),
                           event_tree.root.node_event.wait()])
