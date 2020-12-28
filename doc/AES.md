# Advanced Encryption Standard (AES)

## Basics from italian Wikipedia page

In crittografia, l'Advanced Encryption Standard (AES), conosciuto anche come Rijndael, di cui più propriamente è una specifica implementazione,
è un algoritmo di cifratura a blocchi utilizzato come standard dal governo degli Stati Uniti d'America.

Formalmente, AES non è equivalente al Rijndael (sebbene nella pratica siano intercambiabili) dato che il Rijndael
gestisce differenti dimensioni di blocchi e di chiavi. Nell'AES il blocco è invece di dimensione fissa (128 bit) e
la chiave può essere di 128, 192 o 256 bit mentre il Rijndael specifica solo che il blocco e la chiave devono essere un
multiplo di 32 bit con 128 bit come minimo e 256 bit come massimo.

AES opera utilizzando matrici di 4×4 byte chiamate stati (states).
Quando l'algoritmo ha blocchi di 128 bit in input, la matrice State ha 4 righe e 4 colonne;
se il numero di blocchi in input diventa di 32 bit più lungo, viene aggiunta una colonna allo State, e così via fino
a 256 bit. In pratica, si divide il numero di bit del blocco in input per 32 e il quoziente specifica il numero di colonne.

C'è un passaggio iniziale:
1. AddRoundKey – Ogni byte della tabella viene combinato con la chiave di sessione, la chiave di sessione viene calcolata dal gestore delle chiavi.

Successivamente per cifrare sono previsti diversi round o cicli di processamento: ogni round (fase) dell'AES (eccetto l'ultimo) consiste dei seguenti quattro passaggi:
1. SubBytes – Sostituzione non lineare di tutti i byte che vengono rimpiazzati secondo una specifica tabella.
2. ShiftRows – Spostamento dei byte di un certo numero di posizioni dipendente dalla riga di appartenenza.
3. MixColumns – Combinazione dei byte con un'operazione lineare, i byte vengono trattati una colonna per volta.
4. AddRoundKey – Ogni byte della tabella viene combinato con la chiave di sessione, la chiave di sessione viene calcolata dal gestore delle chiavi.

Il numero di round o cicli di processamento/elaborazione crittografica dei quattro passaggi precedenti è 10 con l'ultimo round che salta il passaggio MixColumns.
La fase di decifratura non è identica a quella di cifratura dal momento che gli step sono eseguiti in ordine inverso.
Tuttavia, si può definire un cifrario inverso equivalente ai passi dell'algoritmo usato per la cifratura, usando la
funzione inversa a ogni step e un differente key schedule. Funziona siccome il risultato non cambia quando si scambiano
la fase di SubBytes con quella di ShiftRows, e quella di MixColumns con una fase aggiuntiva di AddRoundKey.

### SubBytes
Nel passaggio SubBytes ogni byte della matrice viene modificato tramite la S-box a 8 bit.
Questa operazione provvede a fornire la non linearità all'algoritmo.
La S-box utilizzata è derivata da una funzione inversa nel campo finito GF(28), conosciuta per avere delle ottime
proprietà di non linearità.

### ShiftRows
Il passaggio ShiftRows provvede a scostare le righe della matrice di un parametro dipendente dal numero di riga.
Nell'AES la prima riga resta invariata, la seconda viene spostata di un posto verso sinistra, la terza di due posti e la
quarta di tre. In questo modo l'ultima colonna dei dati in ingresso andrà a formare la diagonale della matrice in uscita.
(Rijndael utilizza un disegno leggermente diverso per via delle matrici di lunghezza non fissa.)
Tutte le operazioni sono effettuate utilizzando l'indice della colonna “modulo” il numero di colonne.

### MixColumns
Il passaggio MixColumns prende i quattro byte di ogni colonna e li combina utilizzando una trasformazione lineare invertibile.
Utilizzati in congiunzione, ShiftRows e MixColumns provvedono a far rispettare il criterio di confusione e diffusione nell'algoritmo (teoria di Shannon).
Ogni colonna è trattata come un polinomio in GF(28) e viene moltiplicata modulo x^4+1 per un polinomio fisso c(x)=3x^3+x^2+x+2.

### AddRoundKey
Il passaggio AddRoundKey combina con uno XOR la chiave di sessione con la matrice ottenuta dai passaggi precedenti (State).
Una chiave di sessione viene ricavata dalla chiave primaria ad ogni round (con dei passaggi più o meno semplici,
ad esempio uno shift di posizione dei bit) grazie al Key Scheduler.

Credit to: [AES italian Wiki page](https://it.wikipedia.org/wiki/Advanced_Encryption_Standard)

## Advanced Encryption Standard (AES) Mode

### ECB mode: Electronic Code Book mode
The ECB (Electronic Code Book) mode is the simplest of all. Due to obvious weaknesses, it is generally not recommended.
The plaintext is divided into blocks as the length of the block of AES, 128. So the ECB mode needs to pad data until it
is same as the length of the block. Then every block will be encrypted with the same key and same algorithm.
So if we encrypt the same plaintext, we will get the same ciphertext. So there is a high risk in this mode.
![Image of ECB mode](https://highgo.ca/wp-content/uploads/2019/08/ECB-encryption-1024x408.png)

### CBC mode: Cipher Block Chaining mode
The CBC (Cipher Block Chaining) mode provides this by using an initialization vector – IV.
The IV has the same size as the block that is encrypted. In general, the IV usually is a random number, not a nonce.
The plaintext is divided into blocks and needs to add padding data.
First, we will use the plaintext block xor with the IV.
Then CBC will encrypt the result to the ciphertext block.
In the next block, we will use the encryption result to xor with plaintext block until the last block.
In this mode, even if we encrypt the same plaintext block, we will get a different ciphertext block.
We can decrypt the data in parallel, but it is not possible when encrypting data.
If a plaintext or ciphertext block is broken, it will affect all following block.
![Image of CBC mode](https://highgo.ca/wp-content/uploads/2019/08/CBC-encryption-1024x408.png)


### CFB mode: Cipher FeedBack mode
The CFB (Cipher FeedBack) mode of operation allows the block encryptor to be used as a stream cipher. It also needs an IV.
First, CFB will encrypt the IV, then it will xor with plaintext block to get ciphertext.
Then we will encrypt the encryption result to xor the plaintext.
Because this mode will not encrypt plaintext directly, it just uses the ciphertext to xor with the plaintext to get the ciphertext.
So in this mode, it doesn’t need to pad data.
And it could decrypt data in parallel, not encryption. This mode is similar to the CBC, so if there is a broken block,
it will affect all following block.
![Image of CFB mode](https://highgo.ca/wp-content/uploads/2019/08/CFB-encryption-1024x288.png)


### OFB mode: Output FeedBack mode
The OFB (Output FeedBack) mode of operation (Fig. 4) also enables a block encryptor to be used as a stream encryptor.
It also doesn’t need padding data (the ciphertext is the same length as the plaintext).
In this mode, it will encrypt the IV in the first time and encrypt the per-result.
Then it will use the encryption results to xor the plaintext to get ciphertext.
It is different from CFB, it always encrypts the IV.
It can not encrypt/decrypt the IV in parallel.
Please note that we won’t decrypt the IV encryption results to decrypt data. It will not be affected by the broken block.
It is safe from CPA, but it is easily sysceptible to CCA and PA.
![Image of OFB mode](https://highgo.ca/wp-content/uploads/2019/08/OFB-encryption-1024x516.png)


### CTR mode: Counter mode
At the CTR (Counter) mode of operation as an input block to the encryptor (Encrypt), i.e. as an IV,
the value of a counter (Counter, Counter + 1,…, Counter + N – 1) is used. It also is a stream encryptor.
The counter has the same size as the used block. The XOR operation with the block of plain text is
performed on the output block from the encryptor. All encryption blocks use the same encryption key.
As this mode, It will not be affected by the broken block. It is very like OFB. But CTR will use the counter to be
encrypted every time instead of the IV. So if you could get counter directly, you can encrypt/decrypt data in parallel.
The ciphertext is the same length as the plaintext so padding is not required.
![Image of CTR mode](https://highgo.ca/wp-content/uploads/2019/08/CTR-encryption-1024x530.png)

Credit to: [AES mode](https://www.highgo.ca/2019/08/08/the-difference-in-five-modes-in-the-aes-encryption-algorithm/)

Other credit: [Good Youtube explain](https://www.youtube.com/watch?v=gP4PqVGudtg)