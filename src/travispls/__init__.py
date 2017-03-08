#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import signal
import subprocess
import sys


class AnsiColors:
    CLEAR = "\033[0m"
    BOLD_YELLOW = "\033[1;33m"

    @classmethod
    def enabled(cls):
        """Are both standard output and standard error TTYs?"""
        return os.isatty(sys.stdout.fileno()) and os.isatty(sys.stderr.fileno())


def main():
    """Runs a command in Travis, periodically interrupting the output."""
    parser = argparse.ArgumentParser(
        description="Periodically disturbs Travis to allow long-running builds with stalled output."
    )

    parser.add_argument('-i', '--interval', type=int, default=540, help="Disturbance interval.")
    parser.add_argument('command', help="The command to run.")
    parser.add_argument('args', nargs=argparse.REMAINDER, help="Arguments for the command.")

    args = parser.parse_args()

    # start the process
    p = subprocess.Popen([args.command] + args.args)

    # setup signals
    def sighandler(sig, frame):
        p.send_signal(sig)
        p.wait()
        sys.exit(p.returncode)

    signal.signal(signal.SIGTERM, sighandler)

    try:
        while p.returncode is None:
            try:
                p.wait(args.interval)
                break
            except subprocess.TimeoutExpired:
                disturb()

    except KeyboardInterrupt:
        p.send_signal(signal.SIGTERM)
        p.wait()
        sys.exit(p.returncode)

    sys.exit(p.returncode)


def disturb():
    """Disturb standard error."""
    sys.stderr.write("{prefix}{message}{postfix}\n".format(
        prefix=AnsiColors.BOLD_YELLOW if AnsiColors.enabled() else "",
        message="travis pls",
        postfix=AnsiColors.CLEAR if AnsiColors.enabled() else ""
    ))


if __name__ == "__main__":
    main()
