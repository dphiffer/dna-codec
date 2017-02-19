# dna-codec

Encoding and decoding data into DNA base pairs

## Encode process

`scripts/dna-encode` takes an input file (or reads from `STDIN`) and encodes the data as [DNA base pairs](https://en.wikipedia.org/wiki/Base_pair).

```
dna-encode --verbose --input [filename]
cat [filename] | dna-encode --output [output]
```

## Decode process

`scripts/dna-decode` takes an input file (or reads from `STDIN`) and decodes the base pairs into data.

```
dna-decode --verbose --input [filename]
cat [filename] | dna-decode --output [output]
```

## Dependencies

Uses [Python 2.7](https://www.python.org/downloads/) and the bundled [DNACloud](https://github.com/shalinshah1993/DNACloud), by [Shalin Shah](http://people.duke.edu/~sns37/)

## References

Shah, Shalin, Dixita Limbachiya, and Manish K. Gupta. "DNACloud: A Potential Tool for storing Big Data on DNA." [arXiv preprint arXiv:1310.6992](https://arxiv.org/abs/1310.6992) (2013).
