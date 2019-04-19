pastacli
==========================

Command line interface for interacting with the Provenance Aware Synthesis
Tracking Architecture (PASTA), the system that runs the Environmental Data
Initiative (EDI) data repository.

This CLI implements functionality based on the API documented here:
[PASTAplus](http://pastaplus-core.readthedocs.io/en/latest/index.html)



#### Searching

``` 
$ pastacli --staging search search "q=chlorophyll&fl=title,doi"

<resultset numFound='235' start='0' rows='10'>
    <document>
        <title>North Temperate Lakes LTER: Chlorophyll - Trout Lake Area</title>
        <doi>doi:10.5072/FK2/750effcdcb067fc795d907a66c4b7838</doi>
    </document>
    <document>
        <title>Leelanau Conservancy Lakes Program, 1990-2011</title>
        <doi>doi:10.5072/FK2/12bc966ca5ec152a7cee5a2469b1b8e6</doi>
    </document>    
    ...
</resultset>
```

#### Listing

``` 
$ pastacli --staging 
```

#### Evaluating

``` 
$ pastacli --staging 
```

#### Uploading

``` 
$ pastacli --staging 
```
