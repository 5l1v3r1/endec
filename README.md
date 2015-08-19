# endec

Tiny utility to encrypt and decrypt text data using aes-256-cbc algorithm.

## Concepts

All this script does is playing around with piped data in order to allow
asking for a password.

When data is encrypted - endec asks twice for a password.

Gzip and openssl are used in the background.

Everything is easily customizable.

Encryption algorithm could be switched as well in a matter of seconds.

Tested with Python 2.7.10 and 3.4.3

Windows is not supported.

## Example use

```
cat infile | ./endec (e|d) >outfile
```

## License

[MIT License](https://github.com/twbs/bootstrap/blob/master/LICENSE)
