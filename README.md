# travis-pls [![Build Status][svg-travis]][travis]

![travis-pls](./site/img/travis-pls.jpg)

A little script for keeping very long running jobs online in Travis CI.

## Use-Case

I run some complicated [Packer][packer] builds to build AMIs in EC2. It can often take more than 10 minutes for Amazon
to assemble a simple AMI image. I also run Packer builds to test changes in pull requests and then use custom logic to
tear down the built AMIs until merged to `develop` or `master`.

This script allows my Packer Travis builds to run as long as necessary.

### The Problem

As described in [Travis CI documentation][problem], if a Travis CI build goes longer than 10 minutes without emitting
any output, the build is killed by Travis. "It's okay," Travis docs tell us, "you can use the `travis_wait` command for
long running builds."

Here are a few problems with `travis_wait`:

 - It displays _no output at all_ until the task has completed, and for long running builds, this is a deal breaker. If
   one test case failed pretty early on in your build, you'll have to wait until the end of the build to see what went
   wrong :-1:
 - It isn't available in your deploy scripts, which still have the 10 minute timeout.

### The Solution

A janky Python script which executes any command and arguments passed to it, sending output directly to standard output
and error, sending out the following message (by default) every nine minutes to rustle Travis' jimmies:

> travis pls

It works. Your builds will now stream your output back to you and will only time out after an hour. If you _truly_ need
something that never ever times out, the `-m`/`--max-timeout` flag can be set to `0`, which will cause your build to
last forever. Please don't use this unless you have a paid Travis CI account.

## Usage

```
usage: travis-pls [-h] [-i INTERVAL] [-m MAX_TIMEOUT] command ...

Periodically disturbs Travis to allow long-running builds with stalled output.

positional arguments:
  command               The command to run.
  args                  Arguments for the command.

optional arguments:
  -h, --help            show this help message and exit
  -i INTERVAL, --interval INTERVAL
                        Disturbance interval.
  -m MAX_TIMEOUT, --max-timeout MAX_TIMEOUT
                        The maximum allowed run time in order to be a good
                        internet citizen.
```

By default, `travis-pls` will time out after one hour of execution, and will interrupt every 9 minutes to keep the
build alive.

## Installation

Installation from GitHub is recommended, as the author's personal experience is that PyPI has been historically
unreliable, suffering production incidents as a result.

**From GitHub:**

```
pip install git+https://github.com/naftulikay/travis-pls
```

**From PyPI:**

```
pip install travispls
```

## License

Licensed at your discretion under either:

 - [MIT License](./LICENSE-MIT)
 - [Apache License, Version 2.0](./LICENSE-APACHE)

 [travis]: https://travis-ci.org/naftulikay/travis-pls
 [packer]: https://packer.io/
 [problem]: https://docs.travis-ci.com/user/common-build-problems/#My-builds-are-timing-out
 [svg-travis]: https://travis-ci.org/naftulikay/travis-pls.svg?branch=master
