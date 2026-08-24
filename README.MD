
# BiComic
- Structure
- Naming syntax
- typesetting syntax

BiComic is a file format for multi-lingual manga(or comic)

## Structure

``` mermaid 
---
config:
  theme: redux-dark
---
flowchart TB
  subgraph s99["Episode"]
    n2["pageset"]
    subgraph s98["Language folders i.e 'spa'"]
      n3["typeset"]
      n81[page override]
    end
  end
 subgraph s1["BCM archive"]
    s99
    n9["External Fonts"]
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
    n9@{ shape: procs}
    n5@{ shape: extract}
```

### 

### Fonts

All fonts(even the system fonts) must be initialized with direct url to ttf file by the metadata.json. 
Application search fonts in the system first but it can't find the required fonts because most of the comic fonts are super rare. 
But if you wanna put the font file in the archive. 
Yeah you can do that too. Application compresses the font to remove unnecessary glypes to save some storage but remember this ttf files cannot used accross several archives.

## Syntax

### General

- File names must be always camel-case.
- Files mustn't use any tab characters, only use spaces
- All languages must be flaged in ISO 639-3 standart. 
- Typos? I'm not a llm and i'm using a keybıard that i'm not famişiar, of course I'm gona make so many typos unconciusly. Okay this line is a bit exaggeration that if i don't retype my errors but it still valid

### Episodes

- You can name episodes after hypens
- You can use dots in episode numbers but not in episode names.

### Pages

- Pages must be start with numbers. Numbers should have leading zero('s) for better sorting in some circumstances.
- Hypens in pages are ignored by extractor so you can use for commenting or something else
- Use of Dot(period) and comma is prohibited and must be not using in especially in page numbers before hypens.

### Typesets

Typesets are made of two part: Header that initialize necessary things like fonts; and sets that stores typesetting data.

## Format support

Format support for pageset is like this. You can use any of the marked ones 

- [ ] PSD support
- [ ] PNG support
- [ ] JPG support
- [ ] WEBP support
- [ ] AVIF support
- [ ] HEIF support
- [ ] GIF support
- [ ] SVG support

## Terminology

- `Comic`: An conclutive term for any image book but can be used as any non-CJK comics
- `Manga`: Mostly exclusive to the Japan Comics
- `Manhua`: Chinese Comics
- `Hawha`: Korean Comics
