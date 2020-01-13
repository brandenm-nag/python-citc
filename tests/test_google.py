import googleapiclient.discovery  # type: ignore
import pytest  # type: ignore

from citc.google import GoogleNode
from citc.cloud import NodeState
from tests.cloud_simulator import mock_google


@pytest.fixture
def nodespace():
    return {
        "compartment_id": "myproj-123456",
        "zone": "europe-west4-a",
    }


@pytest.fixture(scope="function")
def client():
    with mock_google():
        return googleapiclient.discovery.build("compute", "v1")


def launch_node(nodename: str, client, nodespace):
    config = {
        "name": nodename,
        "tags": {"items": ["compute"]},
    }

    project = nodespace["compartment_id"]
    zone = nodespace["zone"]
    client.instances().insert(project=project, zone=zone, body=config).execute()


def test_googlenode(client, nodespace):
    launch_node("foo", client, nodespace)
    node = GoogleNode.from_name("foo", client, nodespace)
    assert node.name == "foo"
    assert node.state == NodeState.RUNNING


def test_all_nodes_empty(client, nodespace):
    assert GoogleNode.all(client, nodespace) == []


def test_all_nodes(client, nodespace):
    launch_node("foo", client, nodespace)
    nodes = GoogleNode.all(client, nodespace)
    assert len(nodes) == 1