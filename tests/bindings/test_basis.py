import pytest

from godot.bindings import Basis, Vector3


class TestBasis:

    def test_equal(self):
        v1 = Basis()
        v2 = Basis()
        assert v1 == v2
        v2.x = Vector3(1, 2, 3)
        assert v1 != v2
        v1.x = Vector3(1, 2, 3)
        assert v1 == v2

    def test_repr(self):
        args = (Vector3(1, 2, 3), Vector3(4, 5, 6), Vector3(7, 8, 9))
        v = Basis.build_from_rows(*args)
        assert repr(v) == '<Basis((1.0, 4.0, 7.0), (2.0, 5.0, 8.0), (3.0, 6.0, 9.0))>'

    def test_default_instanciate(self):
        v = Basis()
        assert isinstance(v, Basis)

    def test_build_from_rows(self):
        args = (Vector3(1, 2, 3), Vector3(4, 5, 6), Vector3(7, 8, 9))
        v = Basis.build_from_rows(*args)
        assert isinstance(v, Basis)
        assert (v.x, v.y, v.z) == (Vector3(1, 4, 7), Vector3(2, 5, 8), Vector3(3, 6, 9))

    @pytest.mark.parametrize('args', [
        (),
        (Vector3(), Vector3()),
        (Vector3(), Vector3(), Vector3(), Vector3()),
        (1, Vector3(), Vector3()),
        (Vector3(), 'foo', Vector3())])
    def test_bad_build_from_rows(self, args):
        with pytest.raises(TypeError):
            Basis.build_from_rows(*args)

    def test_build_from_euler_vector3(self):
        v = Basis.build_from_euler(Vector3(1, 2, 3))
        assert isinstance(v, Basis)

    @pytest.mark.parametrize('args', [
        (),
        (Vector3(), Vector3()),
        (1,), (None,)])
    def test_bad_build_from_euler_vector3(self, args):
        with pytest.raises(TypeError):
            Basis.build_from_euler(*args)

    @pytest.mark.xfail(reason='Quat not implemented yet.')
    def test_build_from_euler_quat(self):
        pass

    @classmethod
    def test_build_from_axis_and_angle(axis, phi):
        v = Basis.build_from_euler(Vector3(1, 2, 3), 0.5)
        assert isinstance(v, Vector3)

    @pytest.mark.parametrize('args', [
        (),
        (Vector3(), 0.5, Vector3()),
        (Vector3()), (0.5, Vector3()),
        (1,), (None,)])
    def test_bad_build_from_axis_and_angle(self, args):
        with pytest.raises(TypeError):
            Basis.build_from_axis_and_angle(*args)

    @pytest.mark.parametrize('args', [
        ['determinant', float, ()],
        ['get_euler', Vector3, ()],
        ['get_orthogonal_index', int, ()],
        ['get_scale', Vector3, ()],
        ['inverse', Basis, ()],
        ['orthonormalized', Basis, ()],
        ['rotated', Basis, (Vector3(), 0.5)],
        ['scaled', Basis, (Vector3(),)],
        ['tdotx', float, (Vector3(),)],
        ['tdoty', float, (Vector3(),)],
        ['tdotz', float, (Vector3(),)],
        ['transposed', Basis, ()],
        ['xform', Vector3, (Vector3(),)],
        ['xform_inv', Vector3, (Vector3(),)],
    ], ids=lambda x: x[0])
    def test_methods(self, args):
        v = Basis()
        # Don't test methods' validity but bindings one
        field, ret_type, params = args
        assert hasattr(v, field)
        method = getattr(v, field)
        assert callable(method)
        ret = method(*params)
        assert isinstance(ret, ret_type)

    @pytest.mark.parametrize('args', [
        ('x', Vector3),
        ('y', Vector3),
        ('z', Vector3),
    ], ids=lambda x: x[0])
    def test_properties(self, args):
        v = Basis()
        field, ret_type = args
        assert hasattr(v, field)
        field_val = getattr(v, field)
        assert isinstance(field_val, ret_type)
        val = Vector3(1, 2, 3)
        setattr(v, field, val)
        field_val = getattr(v, field)
        assert field_val == val

    @pytest.mark.parametrize('args', [
        ('x', 'Not a Vector3'),
        ('y', 'Not a Vector3'),
        ('z', 'Not a Vector3'),
        ('x', 1),
        ('y', 2),
        ('z', 3),
    ], ids=lambda x: x[0])
    def test_bad_properties(self, args):
        v = Basis()
        field, bad_value = args
        with pytest.raises(TypeError):
            setattr(v, field, bad_value)

    @pytest.mark.parametrize('args', [
        ('AXIS_X', int),
        ('AXIS_Y', int),
        ('AXIS_Z', int),
    ], ids=lambda x: x[0])
    def test_contants(self, args):
        v = Basis()
        field, ret_type = args
        assert hasattr(v, field)
        field_val = getattr(v, field)
        assert isinstance(field_val, ret_type)
