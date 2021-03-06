# ChaCha20

Like Salsa20, ChaCha's initial state includes a 128-bit constant, a 256-bit key, a 64-bit counter, and a 64-bit nonce,
arranged as a 4×4 matrix of 32-bit words. But ChaCha re-arranges some of the words in the initial state:
```
0x61707865,   0x3320646e,   0x79622d32,   0x6b206574,
key[0,31],    key[32,63],   key[64,95],   key[96,127],
key[128,159], key[160,191], key[192,223], key[224,255],
ctr[0,31],    crt[32,63],   nonce[0,31],  nonce[32,63]
```

The constant is the same as Salsa20 ("expand 32-byte k"). ChaCha replaces the Salsa20 quarter-round QR(a, b, c, d) with
* a += b; d ^= a; d <<<= 16;
* c += d; b ^= c; b <<<= 12;
* a += b; d ^= a; d <<<= 8;
* c += d; b ^= c; b <<<= 7;

Notice that this version updates each word twice, while Salsa20's quarter round updates each word only once.

credit: [ChaCha20 English Wiki page](https://en.wikipedia.org/wiki/Salsa20#ChaCha_variant)