# Salsa20

The core of Salsa20 is a hash function with 64-byte input and 64-byte output.The hash function is used in counter mode as a stream cipher:
Salsa20 encrypts a 64-byte block of plaintext by hashing the key, nonce,and block number and xor'ing the result with the plaintext.

## High level: How do blocks interact?
Salsa20 expands a 256-bit (32 byte) key and a 64-bit (8 byte) nonce (unique message number) into a (2^70-byte) stream.
It encrypts a _n-byte_ plaintext by xor’ing the plaintext with the first _n_ bytes of the stream and discarding the rest of the stream.
It decrypts a _n-byte_ ciphertext by xor’ing the ciphertext with the first _n_ bytes of the stream.
There is no feedback from the plaintext or ciphertext into the stream.
Salsa20 generates the stream in 64-byte (512-bit) blocks and each block is an independent hash of the key, the nonce, and a 64-bit block number;
there is no chaining from one block to the next.
The Salsa20 output stream can therefore be accessed randomly, and any number of blocks can be computed in parallel.

## Medium level: How is a block generated?
The goal of the Salsa20 core is to produce a 64-byte block given a key, nonce, and block counter.
Key = 256 bit (32 byte); nonce = 64 bit (8 byte); block couter = 64 bit (8 byte);
The tools available to the Salsa20core are addition, xor, and constant-distance rotation of 32-bit words.
The Salsa20 core builds an array of 16 words containing the constant word _0x61707865_, the first 4 key words, the constant word _0x3320646e_,
the 2 nonce words, the 2 block-counter words, the constant word _0x79622d32_, the remaining 4 key words, and the constant word _0x6b206574_.

Initial array:
```
0x61707865,   key[0,31],    key[32,63],   key[64,95],
key[96,127],  0x3320646e,   nonce[0,31],  nonce[32,63],
ctr[0,31],    ctr[32,63],   0x79622d32,   key[128,159],
key[160,191], key[192,223], key[224,255], 0x6b206574.
```

Salsa20 now modifies each below-diagonal word as follows:
add the diagonal and above-diagonal words, rotate left by 7 bits, and xor into the below-diagonal words. (_b ⊕= (a ⊞ c) <<< k_).
Salsa20/_r_ continues for a total of _r_ rounds, modifying each word _r_ times.
After these _r_ rounds, Salsa20 adds the final 4×4 array to the original array to obtain its 64-byte output block.

## Low level: Which operations are used?
The Salsa20 encryption function is a long chain of three simple operations on32-bit words:
* 32-bit addition, producing the sum a+b mod 2^32 of two 32-bit words a, b;
* 32-bit exclusive-or, producing the xor a⊕b of two 32-bit words a, b;
* constant-distance 32-bit rotation, producing the rotation a <<< b of a 32-bit word a by b bits to the left, where b is constant.


## Salsa20 Hash Function
The Salsa20 Hash Function takes 64 bytes as input and returns a 64-byte sequence.
First, the Hash Function creates 16 words (in this case: 1 word = 32 byte) from the received 64-byte input. If input is a sequence of 64 bytes:
    input =(b0, b1, b2, ..., b63)
then 16 words are created as below:
* w0 = _littleendian_(b0, b1, b2, b3)
* w1 = _littleendian_(b4, b5, b6, b7)
* [...]
* w15 = _littleendian_(b60, b61, b62, b63)

Then, all 16 words are modified by 10 iterations of the _Doubleround Function_:
    (x0, x1, ..., x15) = _doubleround10_(w0, w1, ..., w15)

Finally, the 16 words received as input are added (as described above) to the modified 16 words and changed to 64 new bytes using the Little endian Function.
The bytes are output from the Salsa20 Hash Function:
    output = littleendian^(-1)(x0+w0) + littleendian^(-1)(x1+w1) + ... + littleendian^(-1)(x15+w15)

### Doubleround Function
The Doubleround Function takes 16 words as input and returns 16-word sequence.
If x is a 16-word input, then the _Doubleround Function_ can be defined as follow:
    _doubleround_(x) = _rowround_(_columnround_(x))

### Littleendian Function
The _Littleendian Function_ changes the order of a 4-byte sequence.
If b is a sequence of four bytes:
    b = (b0, b1, b2, b3)
then the function is defined as:
    _littleendian_(b) = b^0 + 2^8 * b^1 + 2^16 * b^2 + 2^24 * b^3
The _Littleendian Function_ is invertible. It just simply changes the order of bytes in a word.

### Rowround Function
The _Rowround Function_ takes 16 words as input, transforms them, and returns 16-word sequence.
This function is very similar to the _Columnround Function_ but it operates on the words in a different order.

If x is a 16-word input:
    x = (x0, x1, x2, ..., x15)
then the function can be defined as follow:
    _rowround_(x) = (y0, y1, y2, ..., y15)
where:
* (y0, y1, y2, y3) = _quarterround_(x0, x1, x2, x3)
* (y5, y6, y7, y4) = _quarterround_(x5, x6, x7, x4)
* (y10, y11, y8, y9) = _quarterround_(x10, x11, x8, x9)
* (y15, y12, y13, y14) = _quarterround_(x15, x12, x13, x14)

### Columnround Function
The _Columnround Function_ takes 16 words as input and returns 16-word sequence.
This function is very similar to the _Rowround Function_ but operates on the words in different order.

If x is a 16-word input:
    x = (x0, x1, x2, ..., x15)
then the function can be defined as follow:
    _columnround_(x) = (y0, y1, y2, ..., y15)
where:
* (y0, y4, y8, y12) = _quarterround_(x0, x4, x8, x12)
* (y5, y9, y13, y1) = _quarterround_(x5, x9, x13, x1)
* (y10, y14, y2, y6) = _quarterround_(x10, x14, x2, x6)
* (y15, y3, y7, y11) = _quarterround_(x15, x3, x7, x11)

###Quarterround Function
The _Quarterround Function_ takes 4 words as input and returns another 4-word sequence.
If x is a 4-word input:
    x = (x0, x1, x2, x3)
then the function can be defined as follow:
    _quarterround_(x) = (y0, y1, y2, y3)
where:
* y1 = x1 XOR ((x0 + x3) <<< 7)
* y2 = x2 XOR ((y1 + x0) <<< 9)
* y3 = x3 XOR ((y2 + y1) <<< 13)
* y0 = x0 XOR ((y3 + y2) <<< 18)

credit: [Salsa20](http://www.crypto-it.net/eng/symmetric/salsa20.html)