import subprocess
import textwrap

from nodes import node_list, Node


def test_slurm_node_list(tmp_path):
    p = tmp_path / "slurm.conf"
    p.write_text(
        textwrap.dedent(
            """
            # STARTNODES
            NodeName=t3-micro-0001 State=CLOUD SocketsPerBoard=1 CoresPerSocket=1 ThreadsPerCore=2 RealMemory=90 Gres=""
            NodeName=t3-micro-0002 State=CLOUD SocketsPerBoard=1 CoresPerSocket=1 ThreadsPerCore=2 RealMemory=90 Gres=""
            NodeName=t3-micro-0003 State=CLOUD SocketsPerBoard=1 CoresPerSocket=1 ThreadsPerCore=2 RealMemory=90 Gres=""
            NodeName=t3-micro-0004 State=CLOUD SocketsPerBoard=1 CoresPerSocket=1 ThreadsPerCore=2 RealMemory=90 Gres=""
            NodeName=t3-micro-0005 State=CLOUD SocketsPerBoard=1 CoresPerSocket=1 ThreadsPerCore=2 RealMemory=90 Gres=""
            NodeName=t3-micro-0006 State=CLOUD SocketsPerBoard=1 CoresPerSocket=1 ThreadsPerCore=2 RealMemory=90 Gres=""
            NodeName=t3-micro-0007 State=CLOUD SocketsPerBoard=1 CoresPerSocket=1 ThreadsPerCore=2 RealMemory=90 Gres=""
            NodeName=t3-micro-0008 State=CLOUD SocketsPerBoard=1 CoresPerSocket=1 ThreadsPerCore=2 RealMemory=90 Gres=""
            NodeName=t3-micro-0009 State=CLOUD SocketsPerBoard=1 CoresPerSocket=1 ThreadsPerCore=2 RealMemory=90 Gres=""
            NodeName=t3-micro-0010 State=CLOUD SocketsPerBoard=1 CoresPerSocket=1 ThreadsPerCore=2 RealMemory=90 Gres=""
            # ENDNODES
            """
        )
    )
    r = list(node_list(p))
    assert len(r) == 10
    assert r[0] == "t3-micro-0001"
    assert r[-1] == "t3-micro-0010"


def test_create_node(mocker):
    node_data = {
        "nodelist": "vm-standard-e2-2-ad3-0001",
        "statelong": "idle~",
        "reason": "none",
        "cpus": "4",
        "socketcorethread": "1:2:2",
        "memory": "13500",
        "features": "shape=VM.Standard.E2.2,ad=3",
        "gres": "(null)",
        "nodeaddr": "vm-standard-e2-2-ad3-0001",
        "timestamp": "Unknown",
    }
    sinfo_output = "".join(f"{node_data[f]:40}" for f in Node.sinfo_fields)
    mocker.patch(
        "subprocess.run",
        return_value=subprocess.CompletedProcess(
            args="", returncode=0, stdout=sinfo_output.encode()
        ),
    )
    n = Node.from_name("test")

    assert n.statelong == node_data["statelong"]
