import pytest

from godot import RID, Environment, Node, OS


@pytest.fixture
def environment_factory():
    # Environment objects are stubbed on headless server, hence
    # their corresponding RID is always the same default value
    if OS.has_feature("Server"):
        pytest.skip("Not available on headless Godot")

    def _factory():
        return Environment()

    return _factory


def test_base():
    v = RID()
    assert type(v) == RID


def test_equal(environment_factory):
    v1 = RID()
    v2 = RID()
    assert v1 == v2
    # Environment is a Ressource which provides unique rid per instance
    res_a = environment_factory()
    v_a_1 = RID(res_a)
    assert v_a_1 != v1
    v_a_2 = RID(res_a)
    assert v_a_1 == v_a_2
    res_b = environment_factory()
    v_b = RID(res_b)
    assert not v_a_1 == v_b  # Force use of __eq__


@pytest.mark.parametrize("arg", [None, 0, "foo"])
def test_bad_equal(arg):
    arr = RID(Environment())
    assert arr != arg


def test_bad_equal_with_rid(environment_factory):
    # Doing `RID(Environment())` will cause garbage collection of enclosed
    # Environment object and possible reuse of it id
    env1 = environment_factory()
    env2 = environment_factory()
    rid1 = RID(env1)
    rid2 = RID(env2)
    assert rid1 != rid2


def test_lt(environment_factory):
    env1 = environment_factory()
    env2 = environment_factory()
    rid1 = RID(env1)
    rid2 = RID(env2)
    # Ordered is based on resource pointer, so cannot know the order ahead of time
    small, big = sorted([rid1, rid2])
    assert small < big
    assert big > small
    assert not small > big
    assert not big < small


def test_repr():
    v = RID()
    assert repr(v) == "<RID(id=0)>"


@pytest.mark.parametrize("arg", [42, "dummy", RID()])
def test_bad_instantiate(arg):
    with pytest.raises(TypeError):
        RID(arg)


def test_bad_instantiate_with_not_resource(generate_obj):
    # Node doesn't inherit from Resource
    node = generate_obj(Node)
    with pytest.raises(TypeError):
        RID(node)


@pytest.mark.parametrize("args", [["get_id", int, ()]], ids=lambda x: x[0])
def test_methods(args):
    v = RID()
    # Don't test methods' validity but bindings one
    field, ret_type, params = args
    assert hasattr(v, field)
    method = getattr(v, field)
    assert callable(method)
    ret = method(*params)
    assert type(ret) == ret_type


# @pytest.mark.parametrize('args', [
#     (Vector2(0, 0), Vector2(2, 3)),
#     (Vector2(3, 2), Vector2(-1, 1)),
#     (Vector2(-1, -1), Vector2(3, 4)),
# ], ids=lambda x: x[0])
# def test_lt(args):
#     param, result = args
#     calc = Vector2(2, 3) - param
#     assert calc == result

# @pytest.mark.parametrize('arg', [
#     None, 1, 'dummy'
# ], ids=lambda x: x[0])
# def test_bad_add(arg):
#     with pytest.raises(TypeError):
#         Vector2(2, 3) + arg
