# Lemonrunner

Run this forever and stream the results.

The entry point is the Lemonrunner-class, which exposes the run-method. Run
takes an id, a function, and optional key-word arguments for args, kwargs,
timeout, times and interval.

Any function passed to run will be run either forever, or N times, if the times arument is given. Returns, yielded values or exceptions are all retrieved from the monitor-method.

The monitor function of the Lemonrunner-class is a generator which yields each message from each function as they come in.

## Example

```python3
from time import sleep

from lemonrunner import Lemonrunner

def foo():
	raise ValueError

def bar():
	sleep(3)
	return 5

def baaz():
	yield 'abc'

runner = Lemonrunner()

runner.run('foo', foo, interval=1)
runner.run('bar', bar, interval=1, timeout=2)
runner.run('baaz', baaz, times=2)

for id, message_type, timestamp, return_value in runner.monitor():
	print(id, message_type, timestamp, return_value)
```
