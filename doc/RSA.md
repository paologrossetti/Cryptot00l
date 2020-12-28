#Rivest–Shamir–Adleman (RSA)

## Introduction
RSA (Rivest–Shamir–Adleman) is an algorithm used by modern computers to encrypt and decrypt messages.
It is an asymmetric cryptographic algorithm. Asymmetric means that there are two different keys.
This is also called public key cryptography, because one of the keys can be given to anyone. The other key must be kept private.
The algorithm is based on the fact that finding the factors of a large composite number is difficult:
when the factors are prime numbers, the problem is called prime factorization. It is also a key pair (public and private key) generator.
RSA involves a public key and private key. The public key can be known to everyone- it is used to encrypt messages.
Messages encrypted using the public key can only be decrypted with the private key.

## Key generation
The keys for the RSA algorithm are generated the following way:
1. Choose two different large random prime numbers _p_ and _q_
2. Calculate _n = p*q_
3. Calculate the totient: _ϕ( n ) = (p-1)*(q-1)_
    Funzione di Eulero o toziente: funzione definita come il numero degli interi compresi tra 1 e _n_ che sono coprimi con _n_.
    Coprimo: I coprimi ( co-primi ) sono una coppia di interi _(a,b)_ che hanno il massimo comune divisore uguale a 1.
4.  Choose an integer _e_ such that _1 < e < ϕ( n )_, and _e_ is co-prime to _ϕ( n )_ i.e.:
    _e_ and _ϕ ( n )_ share no factors other than 1; _gcd( e, ϕ ( n ) ) = 1_.
    _e_ is released as the public key exponent.
5.  Compute _d_ to satisfy the congruence relation _d * e ≡ 1 ( mod ϕ ( n ) )_ i.e.: _d * e = 1 + x * ϕ ( n )_ for some integer _x_.
    (Simply to say : Calculate _d = ( 1 + x * ϕ ( n ) ) / e_ to be an integer)
    d is kept as the private key exponent.

The public key is made of the modulus _n_ and the public exponent _e_.
The personal key is made of _p_,_q_ and the private exponent _d_ which must be kept secret.
(All parts of the private key must be kept secret in this form)

## Encrypting/Decrypting message
Alice gives her public key ( _n_ & _e_ ) to Bob and keeps her private key secret. Bob wants to send message _M_ to Alice.
First he turns _M_ into a number __m smaller than _n_ by using an agreed-upon reversible protocol known as a padding scheme.
He then computes the ciphertext _c_ corresponding to:
_c = m^e mod n_
Bob uses Alice's public key informations for encryption.
Bob then sends _c_ to Alice.

Alice can recover _m_ from _c_ by using her private key _d_ in the following procedure:
Given _m_, she can recover the original distinct prime numbers, applying the Chinese remainder theorem to these two congruences yields:
_m^(e*d) ≡ m mod (p * q)_ ===> _c^d ≡ m mod n_ ===> _m = c^d mod n_

Encryption involves _n_ and _e_: _ciphertext = (m^e) mod n_
Decryption involves _n_ and _d_: _plaintext = (c^d) mod n_
