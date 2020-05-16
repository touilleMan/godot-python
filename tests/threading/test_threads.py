import pytest
from threading import Thread

from godot import Vector3, SurfaceTool, Mesh, MeshInstance


def test_simple_thread():

    thread_said_hello = False

    def target():
        nonlocal thread_said_hello
        thread_said_hello = True

    t = Thread(target=target, daemon=True)
    t.start()

    t.join(timeout=1)
    assert thread_said_hello


def test_use_godot_from_thread():
    def target():
        st = SurfaceTool()
        st.begin(Mesh.PRIMITIVE_TRIANGLES)
        st.add_vertex(Vector3(-1, -1, 0))
        st.add_vertex(Vector3(-1, 1, 0))
        st.add_vertex(Vector3(1, 1, 0))
        mesh = st.commit()
        mi = MeshInstance.new()
        mi.mesh = mesh
        mi.free()

    t = Thread(target=target, daemon=True)
    t.start()

    t.join(timeout=1)
