# Simple Private Transformer

### Example:

Transform ETH private key to BTC private Key

```
python ./tools/transfer.py priv_transfer priv=c87509a1c067bbde78beb793e6fa76530b6382a4c0241e5e4a9ec0a0f44dc0d3 type=ETH target=BTC
L3wNcWW97SZYV6fb6b5VgoEvtybc9d1Uu6LeiQkVN4Z38VTivKT6
```

Transform ETH private key to EOS public Key

```
python ./tools/transfer.py priv_to_pub priv=c87509a1c067bbde78beb793e6fa76530b6382a4c0241e5e4a9ec0a0f44dc0d3 type=ETH target=EOS
EOS8AXWmo3dFpK1drnjeWPyi9KTy9Fy3SkCydWx8waQrxhnRmwsrR
```

Transform BTC private key to EOS public Key
```
python ./tools/transfer.py priv_to_pub priv=5KLZzSGDG45CfYC1UYjhwL5yAWb84K8Mpbjy87jw1EwqWpafUDD type=BTC target=EOS
EOS56ZcWuPjz2YBg3UtkEWc3gbUCdL6xzMe8SoVwxDo1neUtFXvvA
```
