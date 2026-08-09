# BiComic

- Structure
- Naming syntax
- typesetting syntax

BiComic is a file format for multi-lingual manga(or comic)

``` mermaid 
---
config:
  theme: redux-dark
---
flowchart TB
 subgraph s1["BCM archive"]
        n2["pageset"]
        n3["typeset"]
        n4["metadata.json"]
  end
 subgraph s2["Typesetter"]
        n7["Parse typeset"]
        n8["place texts to pages"]
  end
    n7 --> n8
    s1 --> n5["BiComic Extractor"]
    n5 --> n6["parse metadata"]
    n6 --> s2

    n2@{ shape: procs}
    n3@{ shape: procs}
    n5@{ shape: extract}
```
