## RequestBin - Dark Mode DLC
This is remake of an original RequestBin created by Jeff Lindsay for the internal usage by CTF team Armia Prezesa.

The new features are:
 * dark mode
 * minimalization of source code size
 * custom response text
 * custom response mimetype
 * ability to change bin URL
 * live updates on new requests via websockets - not yet implemented in backend

## Deployment using Docker

On the server/machine you want to host this, you'll first need a machine with
docker and docker-compose installed, then grab the RequestBin source using git:

`$ git clone git://github.com/Lorak-mmk/requestbin.git`

Go into the project directory and then build and start the containers

```
$ sudo docker-compose build
$ sudo docker-compose up -d
```

Your own private RequestBin will be running on this server.

Contributors
------------
 * Barry Carlyon
 * Jeff Lindsay
 * Karol Baryla
 * Pawel Wieczorek
