
from testtools import TestCase


from funky import (
    call_with_globals,
    funkify,
    get_globals,
    mutated_dict,
)

from funky._funky import (
    ImpureFunction,
    pure,
)


class GetGlobalsTest(TestCase):

    def test_no_globals(self):
        def f(x):
            pass
        self.assertEqual([], get_globals(f))

    def test_global_used(self):
        def f(x):
            return x + a
        self.assertEqual(['a'], get_globals(f))

    def test_includes_imports(self):
        def f(x):
            t = TestCase
            return 32
        self.assertEqual(['TestCase'], get_globals(f))


class MutatedDictTest(TestCase):

    def test_empty_dict_no_mutation(self):
        d = {}
        with mutated_dict(d, {}):
            self.assertEqual({}, d)
        self.assertEqual({}, d)

    def test_dict_no_mutation(self):
        d = {'a': 42}
        with mutated_dict(d, {}):
            self.assertEqual({'a': 42}, d)
        self.assertEqual({'a': 42}, d)

    def test_override_value(self):
        d = {'a': 42, 'b': 3}
        with mutated_dict(d, {'a': 2}):
            self.assertEqual({'a': 2, 'b': 3}, d)
        self.assertEqual({'a': 42, 'b': 3}, d)

    def test_introduce_value(self):
        d = {'a': 42}
        with mutated_dict(d, {'b': 21}):
            self.assertEqual({'a': 42, 'b': 21}, d)
        self.assertEqual({'a': 42}, d)


class CallWithGlobalsTest(TestCase):

    def test_no_globals(self):
        def f(x):
            return x
        self.assertEqual(42, call_with_globals({}, f, 42))

    def test_globals_as_parameters(self):
        def f(x):
            return x + a
        self.assertEqual(5, call_with_globals({'a': 3}, f, 2))


class FunkifyTest(TestCase):

    def test_no_globals(self):
        def f(x):
            return x
        self.assertEqual(42, funkify(f)(42))

    def test_globals(self):
        def f(x):
            return x + a
        self.assertEqual(5, funkify(f)(2, _override_a=3))


class PureTest(TestCase):

    def test_pure(self):
        def f(x):
            return x
        self.assertEqual(32, pure(f)(32))

    def test_impure(self):
        def f(x):
            return a + x
        self.assertRaises(ImpureFunction, pure, f)

    def test_pure_method(self):
        class Foo(object):
            @pure
            def f(self, x):
                return x
        foo = Foo()
        self.assertEqual(8, foo.f(8))

    def test_impure_method(self):
        def define_impure():
            class Foo(object):
                @pure
                def f(self, x):
                    return x + self.y
        self.assertRaises(ImpureFunction, define_impure)
