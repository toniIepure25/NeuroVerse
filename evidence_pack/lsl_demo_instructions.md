# LSL Demo Instructions

Terminal 1:

```bash
make lsl-stream-demo
```

Terminal 2:

```bash
make discover-lsl
make validate-lsl-demo
make calibration-lsl-demo
make shadow-lsl-demo
```

Or run the one-command suite after installing `pylsl`:

```bash
make lsl-live-validation-suite
```

EEG replay-over-LSL fixture suite:

```bash
make eeg-lsl-live-suite
```

The demo LSL stream is simulated. It validates real streaming mechanics while
closed-loop adaptation remains locked by default.
