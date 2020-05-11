import time
import pytest
from threading import Thread

import godot
from godot import Vector3, SurfaceTool, Mesh, MeshInstance

def test_gen_mesh_thread():

    done = []

    def target():
        st = SurfaceTool()
        st.begin(Mesh.PRIMITIVE_TRIANGLES)
        st.add_vertex(Vector3(-1, -1, 0))
        st.add_vertex(Vector3(-1, 1, 0))
        st.add_vertex(Vector3(1, 1, 0))
        mesh = st.commit()
        mi = MeshInstance.new()
        mi.mesh = mesh
        done.append([True])
        mi.free()
        
    target()
    t = Thread(target=target)
    t.daemon = True
    t.start()
    time.sleep(3)
    if not done:
        raise Exception("Thread did not return.")
    else:
        t.join()
