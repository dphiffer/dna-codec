# dna-codec

Encoding and decoding data into DNA base pairs

## Encode process

`scripts/dna-encode` takes an input file (or reads from `STDIN`) and encodes the data as a DNA base pairs.

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

Uses the bundled [DNACloud](https://github.com/shalinshah1993/DNACloud), by [Shalin Shah](http://people.duke.edu/~sns37/)
