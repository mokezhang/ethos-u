# Arm(R) Ethos(TM)-U

This is the root repository for all Arm(R) Ethos(TM)-U software. It is provided
to help users download required repositories and place them in a tree structure.

## Fetching externals

The externals can be downloaded with a Python script. The default configuration
is stored in `externals.json` which is a human readable JSON file.

```
$ ./fetch_externals.py fetch
```

The default configuration can be overriddend with the `-c` argument, for
example.

```
$ ./fetch_externals.py -c 21.05.json fetch
```

## Directory structure

The script will build following directory structure.

```
Directory
.
+-- core_platform
+-- core_software
|   +-- applications
|   +-- cmsis
|   +-- core_driver
|   +-- drivers
|   +-- rtos
|   +-- tensorflow
+-- linux_driver_stack
+-- vela
```

| Directory | Description |
--- | ---
| [.](https://review.mlplatform.org/plugins/gitiles/ml/ethos-u/ethos-u) | This is the root directory for all Arm Ethos-U software. |
| [core_platform](https://review.mlplatform.org/plugins/gitiles/ml/ethos-u/ethos-u-core-platform) | This directory contains target specific files and is provided as an example how core software can be built for target platforms. |
| [core_software](https://review.mlplatform.org/plugins/gitiles/ml/ethos-u/ethos-u-core-software) | The software executing on Arm Cortex-M is referred to as _Core Software_. This folder provides a small build system that illustrates how to build the key components for the Arm Ethos-U core software. |
| [core_driver](https://review.mlplatform.org/plugins/gitiles/ml/ethos-u/ethos-u-core-driver) | The Arm Ethos-U NPU driver. |
| [cmsis](https://github.com/ARM-software/CMSIS_5) | CMSIS provides optimized kernels and generic interfaces to the Arm Cortex-M CPUs. |
| [tensorflow](https://github.com/tensorflow/tensorflow) | The TensorFlow Lite microcontroller framework is used to run inferences. |
| [linux_driver_stack](https://review.mlplatform.org/plugins/gitiles/ml/ethos-u/ethos-u-linux-driver-stack) | Example driver stack showing how Linux can dispatch inferences to an Arm Ethos-U subsystem. |
| [vela](https://review.mlplatform.org/plugins/gitiles/ml/ethos-u/ethos-u-vela) | The Vela optimizer takes a TFLu file as input and replaces operators that are supported by the Arm Ethos-U NPU with custom operators designed to run on the NPU. Operators not supported by the NPU are executed in software. |

# License

The Arm Ethos-U is provided under an Apache-2.0 license. Please see
[LICENSE.txt](LICENSE.txt) for more information.

# Contributions

The Arm Ethos-U project welcomes contributions under the Apache-2.0 license.

Before we can accept your contribution, you need to certify its origin and give
us your permission. For this process we use the Developer Certificate of Origin
(DCO) V1.1 (https://developercertificate.org).

To indicate that you agree to the terms of the DCO, you "sign off" your
contribution by adding a line with your name and e-mail address to every git
commit message. You must use your real name, no pseudonyms or anonymous
contributions are accepted. If there are more than one contributor, everyone
adds their name and e-mail to the commit message.

```
Author: John Doe \<john.doe@example.org\>
Date:   Mon Feb 29 12:12:12 2016 +0000

Title of the commit

Short description of the change.
   
Signed-off-by: John Doe john.doe@example.org
Signed-off-by: Foo Bar foo.bar@example.org
```

The contributions will be code reviewed by Arm before they can be accepted into
the repository.

# Security

Please see [Security](SECURITY.md).

# Trademark notice

Arm, Cortex and Ethos are registered trademarks of Arm Limited (or its
subsidiaries) in the US and/or elsewhere.
