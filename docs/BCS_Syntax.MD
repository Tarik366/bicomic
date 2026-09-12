# BCScript Syntax

BCScript is sharing some similarities with [AegiSub](https://aegisub.org/)'s `.ASS` file format. 

## Body

### Override Tags

BCScript has override tags in the `.ass` file format to a certain extent

Here is a list of supported override tags.

> [!NOTE]
> ✅ - Implemented
> 🈸 - Actively implementing
> ⛔ - Not implemented yet
> 🛑 - Will not be implemented in near-future

|                                                  | Tokenizer | Interpreter | Image Processor |
|--------------------------------------------------|-----------|-------------|-----------------|
| \n Soft line break                               | ✅        | ⛔          | ⛔              |
| \N Hard line break                               | ⛔        | ⛔          | ⛔              |
| \h Hard space                                    | ⛔        | ⛔          | ⛔              |
| \i`x` Italics                                    | ⛔        | ⛔          | ⛔              |
| \b`x` Bold                                       | ⛔        | ⛔          | ⛔              |
| \u`x` Underline                                  | ⛔        | ⛔          | ⛔              |
| \s`x` Strikeout                                  | ⛔        | ⛔          | ⛔              |
| \bord`x` Border                                  | ⛔        | ⛔          | ⛔              |
| \x/ybord`x` Extended Border Size                 | ⛔        | ⛔          | ⛔              |
| \shad`x` Shadow distance                         | ⛔        | ⛔          | ⛔              |
| \x/yshad`x` Extended Shadow Distance             | ⛔        | ⛔          | ⛔              |
| \be`x` Blur edges                                | ⛔        | ⛔          | ⛔              |
| \blur`x` Gaussian Blur Edges                     | ⛔        | ⛔          | ⛔              |
| \fn`x` Font Name                                 | 🈸        | ⛔          | ⛔              |
| \fs`x` Font size                                 | ⛔        | ⛔          | ⛔              |
| \fscx/y`x` Font Scale                            | ⛔        | ⛔          | ⛔              |
| \fsp`x` Letter spacing                           | ⛔        | ⛔          | ⛔              |
| \fr/x/y/z`x` Text rotation                       | ⛔        | ⛔          | ⛔              |
| \fax/y`x` Text shearing                          | ⛔        | ⛔          | ⛔              |
| \fe`x` Font encoding                             | 🛑        | 🛑          | 🛑              |
| \1c&H`b``g``r` Primary Color                     | ⛔        | ⛔          | ⛔              |
| \1a&H`b``g``r` Primary Alpha                     | ⛔        | ⛔          | ⛔              |
| \3c&H`b``g``r` Border Color                      | ⛔        | ⛔          | ⛔              |
| \3a&H`b``g``r` Border Alpha                      | ⛔        | ⛔          | ⛔              |
| \4c&H`b``g``r` Shadow Color                      | ⛔        | ⛔          | ⛔              |
| \4a&H`b``g``r` Shadow Alpha                      | ⛔        | ⛔          | ⛔              |
| \an`x` Alignment                                 | ⛔        | ⛔          | ⛔              |
| \k \K \kf \ko \kt Karaoke tags                   | 🛑        | 🛑          | 🛑              |
| \q`x` Wrap Style                                 | ⛔        | ⛔          | ⛔              |
| \r Reset Style                                   | ⛔        | ⛔          | ⛔              |
| Any time related tag                             | 🛑        | 🛑          | 🛑              |
