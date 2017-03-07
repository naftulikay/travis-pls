# travis-pls [![Build Status][svg-travis]][travis]

![travis-pls](https://cdn.meme.am/cache/instances/folder773/500x/75981773.jpg)

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

> 🖕 travis pls 🖕

It works. Your builds will now stream your output back to you and will never, ever time out.

 [img-dolan]: https://cdn.meme.am/cache/instances/folder773/500x/75981773.jpg
 [travis]: https://travis-ci.org/naftulikay/travis-pls
 [packer]: https://packer.io/
 [problem]: https://docs.travis-ci.com/user/common-build-problems/#My-builds-are-timing-out
 [svg-travis]: https://travis-ci.org/naftulikay/travis-pls.svg?branch=master
