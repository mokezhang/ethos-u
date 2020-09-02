# Ethos-u

This is the root repository for all Arm Ethos-U software. It is provided to help
users download required repositories and place them in a tree structure.

## Fetching externals

The externals can be downloaded with a Python script. The default configuration
is stored in `externals.json` which is a human readable JSON file.

```
$ ./fetch_externals.py fetch
```

The default configuration can be overriddend with the `-c` argument, for
example.

```
$ ./fetch_externals.py -c 20.08.json fetch
```

## Directory structure

The script will build following directory structure.

```
Directory
.
+-- core_software
|   +-- core_driver
|   +-- cmsis
|   +-- tensorflow
+-- linux_driver_stack
+-- vela
```

| Directory | Description |
--- | ---
| [.](https://review.mlplatform.org/plugins/gitiles/ml/ethos-u/ethos-u) | This is the root directory for all Arm Ethos-U software. |
| [core_software](https://review.mlplatform.org/plugins/gitiles/ml/ethos-u/ethos-u-core-software) | The software executing on Arm Cortex-M is referred to as _Core Software_. This folder provides a small build system that illustrates how to build the key components for the Arm Ethos-U core software. |
| [core_driver](https://review.mlplatform.org/plugins/gitiles/ml/ethos-u/ethos-u-core-driver) | The Arm Ethos-U NPU driver. |
| [cmsis](https://github.com/ARM-software/CMSIS_5) | CMSIS provides optimized kernels and generic interfaces to the Arm Cortex-M CPUs. |
| [tensorflow](https://github.com/tensorflow/tensorflow) | The TensorFlow Lite microcontroller framework is used to run inferences. |
| [linux_driver_stack](https://review.mlplatform.org/plugins/gitiles/ml/ethos-u/ethos-u-linux-driver-stack) | Example driver stack showing how Linux can dispatch inferences to an Arm Ethos-U subsystem. |
| [vela](https://review.mlplatform.org/plugins/gitiles/ml/ethos-u/ethos-u-vela) | The Vela optimizer takes a TFLu file as input and replaces operators that are supported by the Arm Ethos-U NPU with custom operators designed to run on the NPU. Operators not supported by the NPU are executed in software. |
