# Python library and example programs for E-Stim Systems 2B

For API reference, UTSL. You should read the full source anyway to make sure it doesn't
just set both channels to 100 for lulz. Absolutely no warranty. Read the manual of the
device and follow safety instructions etc.

Example:

```python
from estim_2b import Mode, commander

with commander('COM1') as cmd:
    cmd.set_mode(Mode.CONTINUOUS)
    cmd.set_feel(70)
    cmd.set_level('A', 20)
```

Automatically resets at the start & end of the `with` block.

Tries to stop you from doing anything that's against the protocol, but may not do a
terribly good job at it.

## Example programs

* `sparse_training.py` - Runs the "training" program for approx one cycle, sleeps for a while, repeats.

## Further reading

* [STPIHKAL explais the protocol](https://stpihkal.docs.buttplug.io/hardware/estim-systems-2b.html#serial-communication)