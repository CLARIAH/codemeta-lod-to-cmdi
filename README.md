# codemeta-lod-to-cmdi
CLARIAH Tool Discovery output (LOD -> CMDI conversion)


### makeCmdi.py

use:

`python makeCmdi -i inputfile -o outputfile`

### convertJsonSet.py

use:

`python convertJsonSet -i inputfile -o outputdir`

`convertJsonSet` expects an inputfile with a key `@graph` at the highest level and as the value of this key a `list` of items to convert to `cmdi`.

The output is written to the given `outputdir` as `record_01.cmdi`, `record_02.cmdi`, etc.

`convertJsonSet` uses `makeCmdi` to do the conversion.

