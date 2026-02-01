## Subresource Integrity

If you are loading Highlight.js via CDN you may wish to use [Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity) to guarantee that you are using a legimitate build of the library.

To do this you simply need to add the `integrity` attribute for each JavaScript file you download via CDN. These digests are used by the browser to confirm the files downloaded have not been modified.

```html
<script
  src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.1/highlight.min.js"
  integrity="sha384-5xdYoZ0Lt6Jw8GFfRP91J0jaOVUq7DGI1J5wIyNi0D+eHVdfUwHR4gW6kPsw489E"></script>
<!-- including any other grammars you might need to load -->
<script
  src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.1/languages/go.min.js"
  integrity="sha384-HdearVH8cyfzwBIQOjL/6dSEmZxQ5rJRezN7spps8E7iu+R6utS8c2ab0AgBNFfH"></script>
```

The full list of digests for every file can be found below.

### Digests

```
sha384-DZ/QAiGsDoaeLPHAnnWQ+KAi+ISBMQ1jorfzWY5B6Nck/LEW5BrlynsA7GqEwyq4 /es/languages/arduino.js
sha384-5fqRyRDjJwFL5ud85A5a43LTiHQYvuRA8aoZQfQmjEKTQzQ58xBXhKVxno6hb/yS /es/languages/arduino.min.js
sha384-gRTR/fmk+6+ygbihH/fJvHgmffnOrd/eO7DW5zgu1uN9GBohtDx+OBs0DI0ejigB /es/languages/bash.js
sha384-Pg7b9hYE6kefjcNqAabhv8jOLCVoZubUaM4bZFjUJd0CaaQ14ksDI0GVllMtAF4S /es/languages/bash.min.js
sha384-rqmXEblVZx9ZsNNet5SE9HzCpyLycJlsvFieXpvVMP7rSlQ5g10/r0X/tOuJUzet /es/languages/basic.js
sha384-Z8A67hV3B66k1DT7o/OqP2m0DYQvowlpPFpnONn1omgUmBoqXPbxtd5yjwgn2APh /es/languages/basic.min.js
sha384-xhohaHGp8S443Qn4JZUYAcKqIIl0bQkFA79EUxpbX8GWb5oufdvvSI9ipl/Dasev /es/languages/c.js
sha384-xaTVEdq02jgKStoYDcZD8NhTN1XV/TWpIu4OM53MtMiLl08+e9YJNENo+R/6Nwp0 /es/languages/c.min.js
sha384-rFCBWxbZHxZD51qKR2cdayIcKUSHS3p1PWPIs1kjgsP7lu9ZP32ah/2DoQUm/rTg /es/languages/cpp.js
sha384-+1Koxl0St78gEZW5CpFK+dbLp7yNsfwLzzQUsSGimV4k/RVJUz6YvqtsqtdbJyKf /es/languages/cpp.min.js
sha384-0s8f7nphuRu8IIkFNCeOVZhvbjt7YKZEHl38OjfkCkdtnwIUvwRNbxxUHkCdcYjm /es/languages/csharp.js
sha384-xLfGW0hIBHie9xNFuVroNihI0BdEO8FKxOeCdyJBrO1eM7s5BsQ8F3fLtFydQZ+Z /es/languages/csharp.min.js
sha384-Gmvct15f4Mo9AXQG5bk5w78N1YjBLXXU3KIV7no+mOVnApXlwfw1dwjfueAwljIV /es/languages/css.js
sha384-1D7DbOic0Z5nM2ldSO9O/EsBfsg/5x7X7So1qnMgscI2ucDevptcg7cTvrD9rL0D /es/languages/css.min.js
sha384-QhpRZLeHeNpi6mc0tQD8EPA3ngl6rRNrRFIP2L/+5xw4CAsB6i4XfsybfFBrgSBa /es/languages/fortran.js
sha384-A3+PvZy70E3+xm6wPPF7V67hbjr+poCeuK2CMSUJmhZcFvszluhlVveb2P7VCDBJ /es/languages/fortran.min.js
sha384-y5tpDG/EgM93k2unGm4XFn8l9V12Ru1tnk2TxhduZWqrEqAK86BQlDLuVAILe3OB /es/languages/go.js
sha384-/UGh0AcfdC41Di2LsNVYCPOJ24RfaUWWXniaZoGuM52DaQR7fwStKAHJumI+u5yY /es/languages/go.min.js
sha384-7Px6aOI1M+XCQlR1KDWuNrrFgRbLVtWchPI1dev+c5vNpqRV6TD1N++pG4FVsEGH /es/languages/haskell.js
sha384-sBE/3VGVCFFj0nSxyEPZmpYOSPN/4g8vLcp/k2RJ6qhYwNvywnQM3P926c2LpKGz /es/languages/haskell.min.js
sha384-lk+aAr+DNq8Rz3hXPSZ7ga38GS+tQfXDvexuUnyDCSju1t1SAsLipVIFGlRtcUjE /es/languages/java.js
sha384-5GpB6kfA2w03pZhAUmmNSYvR5pLvne/Rzqc22BmHv+t9ES7ifMX/ZE7x5TBeqW4d /es/languages/java.min.js
sha384-g7t9fKR5Tvod4iWv7BQXN+/JMn5GT9sD6FG3h7Fgl+KCv5k4NnnCzEqUe7BMJ9Mv /es/languages/javascript.js
sha384-f7huPivS1dV2T5V+g0aJpgsY7WBHWCsioIq30tpNoXGizD65fWJYGuXXVPNI52VB /es/languages/javascript.min.js
sha384-8CRS96Xb/ZkZlQU+5ffA03XTN6/xY40QAnsXKB0Y+ow1vza1LAkRNPSrZqGSNo53 /es/languages/json.js
sha384-UHzaYxI/rAo84TEK3WlG15gVfPk49XKax76Ccn9qPWYbUxePCEHxjGkV+xp9HcS/ /es/languages/json.min.js
sha384-74O59Gvm0duu3aXH7S8RHhqn8YvAF1JlgCdNDq5MaClY/f/0bMs4zryv55Whwp2c /es/languages/kotlin.js
sha384-+aJFpyNBGTRiXRDN6BLrctauQBKExwSosxOiHLUYReXKTsckW/RgMavqX6W+zTBL /es/languages/kotlin.min.js
sha384-Ap4gnRYGNAeKXru7neutEvzrhsYnnP1suT5zxW2zdmv6rCl43QzqqLEJ1F3kZWWm /es/languages/latex.js
sha384-bx4oC5pPCnrSzdPzDg3L9UsoJWiptFFwoGWKup6bRk82EzPFrquQa7T7I9iDwnXa /es/languages/latex.min.js
sha384-5TnIBSbRIGDilxscXgaTNLZ8PZ9u7TEBPzF8b9z+wrbTN3e89MbD9zSSuDVdbDFj /es/languages/lua.js
sha384-HCBq0pjgKyOc3FNX31to33MxfNYza3HCbHLfWwdsnkH5r/VmmXTlRrvWSHTJyYvA /es/languages/lua.min.js
sha384-FEDx4j8b0w8PZYSgOHx7ri0VswVyBFJKmnbMEUOVYY37i0PNrOuWE1A7t0CJZnzk /es/languages/mathematica.js
sha384-s9OhOZLci2dao+WT5xmnxIgAID9YQRqb/zWb9UoLnO6p41wXb2/0HlhB3pgXFk+A /es/languages/mathematica.min.js
sha384-2P4mzPjIYmPuF0LdW1jpx1VKc6cx2l3smcGqNNHRj2jIvGGsiAUGklcbWkDt10Hh /es/languages/matlab.js
sha384-1V+EHXAHVnBm9cEy3kpZDOO8LI9tOkHylYgT6gQdG5QRJVA8lIlLt/eQqfhiEPnr /es/languages/matlab.min.js
sha384-gPjhD9B3eKMKoi+i3tYG1UcMUivCp9B5pM+altrGmMCGtc/1044OoB91n3AHDce4 /es/languages/ocaml.js
sha384-K1wF0NzhmShaNd0mazLwrxnm0VT2wtNGclvFeDfuYRMM1g92YApMTm+Zknp7Jt+C /es/languages/ocaml.min.js
sha384-4OPZSHQbxzPqFMOXnndxQ6TZTI/B+J4W9aqTCHxAx/dsPS6GG25kT7wdsf66jJ1M /es/languages/php.js
sha384-VxmvZ2mUpp1EzFijS40RFvIc7vbv/d5PhMxVFG/3HMpVKD4sVvhdV9LThrJDiw9e /es/languages/php.min.js
sha384-i6sPjmXfHWLljAXTYYk0vBOwgsUnUKnKXKH41qzc9OMhaf5AFZqXH7azX4SYdUiR /es/languages/plaintext.js
sha384-OOrQLW97d+/1orj9gjftwbbQyV8LNAcgagqVKBhUYA08Hdi5w0p6VoB3yt2k7gnG /es/languages/plaintext.min.js
sha384-Cmq5lORXzyHraasLNqmfchH07JRXyEmjDF+j6tSggoXjYHwtgX/ySW6kkRytM5uu /es/languages/python.js
sha384-ZV5sgX70bBgLkDR5Mtox5UsbJedBc39hRKPdvTw6miK4lSkE/wv94cLY2iyZb/sB /es/languages/python.min.js
sha384-JFRCn12yvr0NDhxPY8oZDk/G2Tjm7bGmqXy28Y0bq4J7D8mKha6jQJOXMB5wtTVr /es/languages/rust.js
sha384-JbkB8w/DGGyx29PIwSq8c/ZeiJB9T/X4mVAZFEyBiNlEAas98Q2NxpBPUlNIlE71 /es/languages/rust.min.js
sha384-R67rULqIohpEyV6aFbjxRv7xhK8v/KteX4cvOFmPcnZ2MTf65Zua+2DzB9MqqXuO /es/languages/scss.js
sha384-WMy5VYgOMFAnHhPJXVDCQ/Y/QPlUrBqNVPtFH6/gGg2F4uaAowyQ0y/9zWEeGpJe /es/languages/scss.min.js
sha384-1mmBZmAs44b6FtD9wpMiLJa8bLZgZv9xoAhngN6B5Q22y9CtcsU2lat0zlRtyVgy /es/languages/shell.js
sha384-u9PV7oWG/lZlm+GnftX7kn0w4b8rRfFxSv5SmJJPHWKGI03rz6VLqgZdQ1B5ez6b /es/languages/shell.min.js
sha384-s1ZfN6xtlNKAZux8QYAG7upUsit3RwK5XDoCAN3g6Kj33RrIqbmkuGjdNF9RvzPM /es/languages/sql.js
sha384-y25cn06synxhYnlKVprZdpakuFWVrm2jvn8pqiF4L85a05CI/6bNeT2+qXbUYIyW /es/languages/sql.min.js
sha384-sfRYvVvcwsysqkDUscQ/SqsFOSvNGkGX5vm/yKMHdTwTd7A++Pqx1QpJK0bGebPD /es/languages/swift.js
sha384-9NAaCxdhTO7TX6fYeUHyt+NC3ledirZOADyWdinDCTN1taeqj8sLLYqjE8YMf4Na /es/languages/swift.min.js
sha384-Z61gsCS2W7Q+3fT1fdya/Sz4wlmsotT9iEGzgIlNqP0soaKH1NzysutxWp08Hh3E /es/languages/typescript.js
sha384-Tv4mr9B7b+x2IynRXW/xcAxUj1+AoN9zyp0n9BWE1Nle3Zfm/zUeEztNLhIRjgE7 /es/languages/typescript.min.js
sha384-9ECFzM+oWDye4s/MFx3QUXGo4mW43+SyLpWUDeQtWup6GZJ+KHFxVS89PmZt/fzl /es/languages/xml.js
sha384-PQrsaWeWrBiE1CFRw8K335CaJuQRTjDGm73vn8bXvlwaw6RyqWObdvMTBS8B75NN /es/languages/xml.min.js
sha384-7HTgKp/l2rzlyrh5vUfbfZVy+Wx1lKO4iGmfqvakienApv21u55lo+Vi+iVg4jY0 /es/languages/yaml.js
sha384-4smueUtgWTorlNLbaQIawnVCcIAuw82NetPOGWN5PbZT/pMr0rjvZXj0EUzJV1nr /es/languages/yaml.min.js
sha384-suZoQknnQ0DBASFb5XFnOEH5yo/3puJ8QB7Si5imwbDpwqTHUE97sax+2gSz1y5Y /languages/arduino.js
sha384-Fh/jSSfDM8TBxrEe/yPhSI9FpoMT/3TL5ib1pmehS1cHspQ9SWRYbUSW5QCCbI56 /languages/arduino.min.js
sha384-Jrkpn2hK0TY04skYBXB9fj7mMpKYy7g726cPwXGXf6mdBXnFlTDXFduxikMCRXT7 /languages/bash.js
sha384-BbT8tZtvkh8HPXIvL5RtzuljBwI3gR5KIdYxZyYSyI5C/+KNAGdzAiexvmxuroag /languages/bash.min.js
sha384-bnpCuTpfS8ukuVLhfvZeux01GjkQSo1jSHbvMeO+AHZOiiFEi0UKrwxAUMYDA0KQ /languages/basic.js
sha384-eiOqb/ds7X3JkCFzpDHXdBBL35GrdT1oz3+qs3L2GqIH8P0/BRhJ4AqYHFTlGhcx /languages/basic.min.js
sha384-lAz0Eyld5DmFJB7cxaZonrkUJzGefh+K3niV5d7+vzzS7/P7FEeCJeLNXzMjeo+N /languages/c.js
sha384-tMmX0hBMZeMrZhX6dUNxA94/DNJLl70ao6qu2N9+b/6Ep9Y2e1pBzVjxtLygIB+d /languages/c.min.js
sha384-Z5Ja/rxBluJ4iPYwJYn2numfw2XFmlp3qLL1aJ1SZqyTjKWwMh9yWfpNCOqf3vAm /languages/cpp.js
sha384-B711MHXDqRvH/pKkxJk84RyRt9g0qyAJFsu2XukZKoCdnEiBmA6Aq9fO23ZCS7qk /languages/cpp.min.js
sha384-NTF0oluJbKDCxwGTujk+IsRQRbf+waUyDilA5GhOA+VSoxhyApQpmDWMjxfFO3dt /languages/csharp.js
sha384-Z+o7SU/ldIEIdOIqpMV+9s2n8EE1rZTFSRv5Sd7rlaSoPTpyflmmZ/oRb6ycw/2s /languages/csharp.min.js
sha384-bsb3QmLtUiyaiHwtrL4YoAVI9yLsjyqxgoAsk4Zd+ass9rSK1WWRiCDSu/hm8QRp /languages/css.js
sha384-0XGvxIU7Oq1DQMMBr1ORiozzBq3KpZPE/74mJysWRBAop1dZ9Ioq/qRWe8u30Ded /languages/css.min.js
sha384-SOuDxJBMFmbQBxU18ksxNru61DqhZzqKhFe262U4+vnCSGdXGrEZw7miT+/DqeTo /languages/fortran.js
sha384-js87axhH2Q+jkxUjpaX7DgtCMTO45eaDvzB5d4JvbuVwLp0w3b9We/TfVy2qJaK4 /languages/fortran.min.js
sha384-uh0SMHiaDpf+y9t0NE6+t9c3aMlzs8mHPxmkEU3fY12P481V2wNrKoxPMlKVG61k /languages/go.js
sha384-HdearVH8cyfzwBIQOjL/6dSEmZxQ5rJRezN7spps8E7iu+R6utS8c2ab0AgBNFfH /languages/go.min.js
sha384-rhn33/u/Bx9ACz9kwMH5G73O/ZVdpbb67Tl4IdfxFMxQVLxhMnd1rjiYHtmFPUdo /languages/haskell.js
sha384-Z7NJwTxw7Rkjd5VqLt3KR5VyFUlCThJa7/4khFskUKDYPBiuk/UcS10ApTNW2Xxf /languages/haskell.min.js
sha384-Dprg6CdFFkimxaHg7qM7njVaWLMlOLqughixPERBDbm0cHdX6rKujTnJReof8O6m /languages/java.js
sha384-e+59xEZvRMXSRGD31B3HOBGAGqhhs+bbkxCqPuJDkSX5QGneIGTIfwdYJckTN3AO /languages/java.min.js
sha384-yxv7Fv9ToggiLsR67t98hV5ZRup6XX6xL1Rkbi/cGV5J8y7fosCi9POqlBkiBWFg /languages/javascript.js
sha384-tPOrIubtDHoQU7Rqw0o88ilthGO0/4xEZGB47XrQKWhrc1/SchwsDx+AP74u4nk0 /languages/javascript.min.js
sha384-pUlqdjoNePvHvdi7GVKJJnh/P2T3EvXXodl5j0JtTkbNC4DRH7gwGbcHFa84bFOP /languages/json.js
sha384-3C+cPClJZgjKFYAb0bh35D7im2jasLzgk9eRix3t1c5pk1+x6b+bHghWcdrKwIo3 /languages/json.min.js
sha384-vIyPs+G4S+ut5NV5tBIN5/E17wBiWbTTkFPPFbBC+r/FZOD95/fbcSzzeo00bE3x /languages/kotlin.js
sha384-7abn027YsNDPFilpW9aLlNUanPrq7Ht81zKQL9MKQq6/nkKrLczChRK5OA8GSKep /languages/kotlin.min.js
sha384-gC1LLqQxzTtslF1/nhSmFhIyScy7u0VnfVPDE45XlK+Ed/wgeOK0zae/DRDGNTDs /languages/latex.js
sha384-A8E38+eenPg19mMk5Ikv1fetaPL/yA2OsGR3hFs9TeeBX+zQ8u5bZNsPKmlFHwN4 /languages/latex.min.js
sha384-IQZHDTDQQ0zpXf1FfEYOFIfjZrBbLbNXYCn4zukU6u9mLf6JI36vvIRaV6/d175T /languages/lua.js
sha384-dbTI+BVfiAlIfjWMYrH83f/x/GYSKbujaX4g4F7q5YxbGtlS7qTLcwBQQvDdsGf6 /languages/lua.min.js
sha384-fX11ESuAxHunHWn4oHvM1CUUeacOuMeK0bbZHeKRWM8ix6OH11eH6mdZE4FA2UuW /languages/mathematica.js
sha384-y1+UZ2Tj8YGxk8pltI2Xo0e17nA9sBMyynUZGHY1ZUDaVMBQCB91/ci3nYxZbJ4u /languages/mathematica.min.js
sha384-+IiDNSrq9hiDOlzPG1CxaS5ojDqswYZmy3eN4ChCbwEk2UpQwQLk+xkaVjs99yzx /languages/matlab.js
sha384-lq1I9kuTT+eCtMpqcUeHyTatwv3ccB90NXm1b3I7ju0ueJKdD4rdRNMSGvhJpKBg /languages/matlab.min.js
sha384-FMuGqFdDMUSuNDMdrHPQJ5mnHDcvRdz8JaSHcx9gKYEgRLWLJjrXG7VCqkP2Z9N9 /languages/ocaml.js
sha384-Ox9CQ7lFdK85QgO6+LBGHukeEXutfvnC8BSMg78nFV2OqScEbL4inhxDrfcAFdmO /languages/ocaml.min.js
sha384-0XBmTxpMLuDjB2zdfbi3Lv4Yokm2e1YFGZ9mCmI5887Kpi23jMF5N7rPrf0GdoU/ /languages/php.js
sha384-Bv/Sxv6HlOzYOdV1iQpJTG3xiqGWIIMq9xsFfEX8ss7oNWMgKqOa/J2WSFG2m7Jd /languages/php.min.js
sha384-MZKv9uidO1+VnHz8xWxPv6ACuLO5t823eanvTcKYnmi/ocdVYD8zKZNTxmF0nKEM /languages/plaintext.js
sha384-Z9EdtPaC8UiXHEq1WuQTdvqT+FwjLwaVTIwTCZW/dGfiU9nbF8Shvltrhqtw83Qb /languages/plaintext.min.js
sha384-ueSSFZFqg7cVD0dpEqIk9EefJiJUYan0PH6I8u/p+bNLLx7dMs4J2keMaFXqCN8P /languages/python.js
sha384-eXRt+aAa2ig1yFVDQCLis8k9s/1dikTcigj+/R07yNdIxc8BAG/b1uHDyEW3of17 /languages/python.min.js
sha384-4hMItQrXDnquJWRbDiZ+cP4udu1pcJlCVFg3Ytv9OgWNbpIwzizsWbIwzA1BAJrI /languages/rust.js
sha384-kENps59cKQW5DV3vOEzpSp6tfGzWGpPYKz748i4gGziVSjieRtupNNu/WEwG3s8n /languages/rust.min.js
sha384-e5MJZgawCv4c+BexmFUMVQU6dLcIOXdieG/a1FPCIgnlGfBIEUUcFMMo+UrKMOtN /languages/scss.js
sha384-BYdYy4D3IX6eNNlKqsviUjxC6EqavvNwCVDMzmie3QXyArWdCQf+VvvFo4ciaNaW /languages/scss.min.js
sha384-BanM6jNzM3hgNw0Vu3gSe58a3MK3PSlMUzh5s8QaaDzIvTWgB0jNetV3rNxteKHy /languages/shell.js
sha384-mSZF08WaP0Llc4GMwE0KA2V9yfZQimO5PvfcXf2AATDdqri3Q7IdV7pfbhVPJCHV /languages/shell.min.js
sha384-2sXmcW3eKeNDWiLtuq9NgFJC4NsLBN/fDTzZevmcgBrSERv6iO/k+c7r9T09Fb8J /languages/sql.js
sha384-jrnLoVn13sB+/dTfoAYVPhg0tYGQzzuzSGP3WTk8OvKAY0hDejpUXFYYI3bohAyW /languages/sql.min.js
sha384-+juhAXbxlgltos7eNuzta0Y7hfKqGQftMcEEStYqBJftSEdIiLd/FaviI8hs4d86 /languages/swift.js
sha384-CCauhmYx0fwWViYO6uiTII5shLTfiY/OzxKmLRTeCp8Ok81I2nXZS2Gb9lJVOSPC /languages/swift.min.js
sha384-8v3YMaXFO9cmTNxsHWqwn9wJsV1jVO7rwx4huxqlEQpT/P2tuDbtm+Hs0EdYqu0a /languages/typescript.js
sha384-df1w1nJ43GNwmgbSCrT8YFIYyqFAm+lzj+b6ofuziX8Cfdg9QHFwbORDgAaj//wi /languages/typescript.min.js
sha384-Pgzg6a405W6U1xFjjSs5i8d7V81Tmt/TYn8HFOa+u1psDc8cbs8nC7BuyNXbWWRK /languages/xml.js
sha384-FQjSArDMJE4WMAJGcCNAV+IXIOljcIxM3UFAD2vxjedWmBnnDaAyqRG7AQHf/uM/ /languages/xml.min.js
sha384-6GXi9L5BnOWPU6bzwYL78Zscp23qyDdMLZpZvp4mLzvF2qt0eY/DfsPHiFVXq4hv /languages/yaml.js
sha384-A/iMReLA0Bo3tLydBIoOQXQzYnrwL90jkHYUubrtERUGCbIuU7U0EHge0Xd2s5sr /languages/yaml.min.js
sha384-KmQlP00HL8K/JJdSmSyznawqE3qGGBveo2Dl9w3RFdWl+3pjNUDc+04iKyiijfux /highlight.js
sha384-g9IJ1RSVfF3FxiGM1mqS7ft8wt6v9x/qsObhlYFuwPwxDwnMo0s6y50JH+6GPPfI /highlight.min.js
```

