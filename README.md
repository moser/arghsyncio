# Argh-syncio

A couple of experiments to see how synchronous & asynchronous stuff can
work together.

## ab

[ab](https://linux.die.net/man/1/ab) is a simple HTTP "benchmarking" tool.
It's no good for doing real load tests (because it is inefficient on its own
and will skew results) but it's OK for hitting a service with a couple of
concurrent requests.

### Installing
On MacOS it seems to be installed by default (could not check)

On Ubuntu/Debian, run `sudo apt-get install apache2-utils` to install it.
