# get funky

*Is hidden state getting you down? Don't gett down, get funky.*

## what?

This is a proof-of-concept Python hack that exposes the global dependencies of
a function as optional keyword arguments, allowing you to easily vary them in
tests.

## why?

Say you've got code that looks like this:

```python
def f(x):
  if global_config['HAHA']:
     sys.stdout.write('laugh\n')
  else:
     sys.stderr.write('cry\n')
```

It's wonderful, and probably correct. But how do you test it?

Essentially, you have to patch out all the references to external objects and
replace them with fakes for testing.  If you're using
[mock](http://mock.readthedocs.org/en/latest/), you might write something like
this:

```python
@mock.patch('sys')
def testF(self, mock_sys):
    with mock.patch.dict('mymodule.global_config', {'HAHA': False}:
        f('whatever')
    mock_sys.stderr.write.assert_called_with('cry\n')
```

And that works for a lot of people.

What you're doing is varying `os`, `sys`, and the `global_config` dict and
then seeing what `f` does in response. Which is great: that's what tests are
supposed to do.

But, you can make this explicit by making those things _parameters_ of f.
That's where `funky` comes in.

```python
funky_f = funkify(f)

def testF(self):
  mock_sys = mock.MagicMock()
  f('whatever', _override_sys=mock_sys,
    _override_global_config={'HAHA': False})
  mock_sys.stderr.write.assert_called_with('cry\n')
```

Why is this better?

It hides the details of patching and state mutation from your test, allowing
your test to focus on what happens when you vary the inputs: which are *all*
expressed as parameters.

Not only does this remove the big stack of decorators, but it makes it easier
to see what exactly your tests are covering.
