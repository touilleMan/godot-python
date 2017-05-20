import pytest

from godot.bindings import Array, Node, Resource, Area2D, Vector2


class TestArray:

    def test_base(self):
        v = Array()
        assert type(v) == Array

    @pytest.mark.parametrize('arg', [
        Array,
        # PoolColorArray,
        # PoolVector3Array,
        # PoolVector2Array,
        # PoolStringArray,
        # PoolRealArray,
        # PoolIntArray,
        # PoolByteArray,
        # PoolRealArray,
        list,
    ])
    def test_equal(self, arg):
        arr = Array()
        other = arg()
        for item in [1, 'foo', Node(), Vector2()]:
            arr.append(item)
            other.append(item)
        assert arr == other


    @pytest.mark.parametrize('arg', [
        None,
        0,
        'foo',
        Vector2(),
        Node(),
    ])
    def test_bad_equal(self, arg):
        arr = Array()
        assert arr != arg

    def test_repr(self):
        v = Array()
        assert repr(v) == '<Array([])>'
        v = Array([1, 'foo', Vector2()])
        assert repr(v) == "<Array([1, 'foo', <Vector2(x=0.0, y=0.0)>])>"

    @pytest.mark.parametrize('arg', [
        42,
        'dummy',
        Node(),
        Vector2(),
        [object()]
    ])
    def test_bad_instantiate(self, arg):
        with pytest.raises(TypeError):
            Array(arg)

    @pytest.mark.parametrize('arg', [
        Array(),
        # PoolColorArray(),
        # PoolVector3Array(),
        # PoolVector2Array(),
        # PoolStringArray(),
        # PoolRealArray(),
        # PoolIntArray(),
        # PoolByteArray(),
        # PoolRealArray(),
        [],
        (),
        [42, 43, 44],
        ('foo', 'bar', 'spam'),
        (Node(), Resource(), Area2D()),
        [Vector2(), Vector2(), Vector2()],
        (Node(), Resource(), Area2D(), Vector2(), 'foo', 0),  # Enjoy the mix
    ])
    def test_instantiate_from_copy(self, arg):
        arr = Array(arg)
        if hasattr(arg, '_gd_ptr'):
            assert arr._gd_ptr != arg._gd_ptr

    @pytest.mark.parametrize('args', [
        ['append', type(None), ('bar', )],
        ['clear', type(None), ()],
        ['count', int, ('foo', )],
        ['empty', bool, ()],
        ['erase', type(None), ('foo', )],
        ['front', str, ()],
        ['back', str, ()],
        ['find', int, ('foo', 0)],
        ['find_last', int, ('foo', )],
        ['has', bool, ('foo', )],
        ['hash', int, ()],
        ['insert', type(None), (0, 'bar')],
        ['invert', type(None), ()],
        ['pop_back', str, ()],
        ['pop_front', str, ()],
        ['push_back', type(None), ('bar', )],
        ['push_front', type(None), ('bar', )],
        ['remove', type(None), (0, )],
        ['resize', type(None), (2, )],
        ['rfind', int, ('foo', 0)],
        ['sort', type(None), ()],
        # ['sort_custom', type(None), (obj, func)],
    ], ids=lambda x: x[0])
    def test_methods(self, args):
        v = Array(['foo'])
        # Don't test methods' validity but bindings one
        field, ret_type, params = args
        assert hasattr(v, field)
        method = getattr(v, field)
        assert callable(method)
        ret = method(*params)
        assert type(ret) == ret_type

    def test_len(self):
        v = Array()
        assert len(v) == 0
        v.append('foo')
        assert len(v) == 1

    def test_getitem(self):
        v = Array(['foo', 0, Node()])
        assert v[0] == 'foo'
        assert v[1] == 0

    def test_getitem_slice(self):
        v = Array(['foo', 0, Node()])
        assert isinstance(v[:-1], Array)
        assert v[1:] == Array([v[1], v[2]])

    def test_outofrange_getitem(self):
        v = Array(['foo', 0])
        with pytest.raises(IndexError):
            v[2]

    def test_setitem(self):
        v = Array(['foo', 0, Node()])
        v[0] = 'bar'
        assert len(v) == 3
        assert v[0] == 'bar'

    def test_outofrange_setitem(self):
        v = Array(['foo', 0])
        with pytest.raises(IndexError):
            v[2] = 42

    def test_iter(self):
        items = ['foo', 0, Node()]
        v = Array(items)
        items_from_v = [x for x in v]
        assert items_from_v == items

    def test_append(self):
        items = [1, 'foo', Node()]
        v = Array()
        for item in items:
            v.append(item)
        assert len(v) == 3
        assert v == Array(items)
