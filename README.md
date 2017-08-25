AirCast
============

A bridge between AirPlay (via [shairport-sync](https://github.com/mikebrady/shairport-sync)) and Chromecast devices, allowing you to stream music seamlessly between your iDevices and your Chromecast or Chromecast Audio.

Quick Start
------------

If you don't have dedicated hardware (e.g. a Rapsberry Pi) to run aircast on, you can run the bridge locally inside a VM
on your machine using [Vagrant](https://www.vagrantup.com/).

```
$ git clone https://github.com/ains/aircast.git
$ cd aircast
$ vagrant up
```

The AirCast Airplay emulator should now be visible on your local network, with the same name as your chromecast device.
