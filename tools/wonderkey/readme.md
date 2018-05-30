# Wonder Key -- generate your favor Key / Address

### Install

```
make dev-install
```

### Example

#### Priv


```
python tools/wonderkey/wonderkey.py wonder type=EOS pattern=".*3$"
Found: 5JmCgpirreuxtGk58KU7nkzsd2tqdh4H82iK8erQoeV5RNG22c3
Found: 5Je2S6GH1d4i446ZGTTQsFDMiJaRYhyJpxfsF2rh5odbsGbWTB3
Found: 5KSujLLfvVcfAXRpgpbe3MuM4BTVricm7Yghbzq7uLSphJoVEX3
```

#### Pub

```
python tools/wonderkey/wonderkey.py wonder_pub type=EOS pattern=".*V$"
Found: EOS6nvpZgMLHYsuBq4QbZb7fB6SLnZNH1si2iryutxXjzBvu57i2V with private key 5Kdxpou4j5uwCrXkv8cTmLb3fhKH66b7HH4LMJnH1uowNtSV6hQ
Found: EOS8YeSqqKNv7FpyiRaSuFx5w9EgWCEn1vUidv78PBn144Goj3vDV with private key 5JndWUDK91EUnPeMtuHjxXckuVcxcCmknsicWNRb8mdNkZ8tBJG
Found: EOS7JgaFdizjDuXhogp8Y5nFYXeDRFHawH1VQrKzDnFsBqXszUYQV with private key 5JwqCeqbhFAQPD6gTjQWw9QDu1AcUzGQjxaZGUSk1dmT4ERKixk
Found: EOS6JbTQ27GkCbHvqB5nYAybkzFh4RSLiCGcebQcNhCQxgK5QrHHV with private key 5Hw5nDxYHMH8GMRxDRW3JYHATDnC374Sf6291uHdBuoU4z4qGpQ
```

#### Address

```
python ./tools/wonderkey/wonderkey.py wonder_address type='EOS' pattern="EOS.*"
Found: EOSAHSH2fuSwSTPcCCnk8gYLtK1oTj8FvTqC with private key 5KXeyRrNHuU9mdM9KvJ2drTjcjeDQe6JaxJ9pYKgeXEekiwJ3a3
Found: EOSC11hm7irgwFn3oGYeeLoc6yMxzCs4ytvz with private key 5KcqsEZRkNTfCj55tZ9hP2qfmQ94ym8MfgMBTUGVZAWECtRzqkN
Found: EOS5fFMqtdwW4QidrZjN2Ue9oLbUtrLAsJTf with private key 5JLWkMixY9aC8cBMS4JUsLvgKQGMZu6uUdrmkU3naVnsGgk2Suj
Found: EOS7vmJgy2tKBfU9GEczEG4eCYaSWVvEXhtH with private key 5KdigihfupGXJ8D5x2rekqLpc4nnu196AuHfSaqSgBkTLpm9mfH
Found: EOS81jBBjyeF6CKvVenxqAS12AAn3sn4sfqj with private key 5JN3TKPUxKAC9vy1oYDXkAc8tcvbzGjMjW7ZVU91kX2LNeh3ChZ
```
