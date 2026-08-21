# TypeSets

Typesets are the text-based side of Bicomic and stores in the archives corresponding language folder in `.bcs` format. 
It's saves the text layers in PSD files to store in a more appropriate and optimized way 
to be more agile and easy-to-implement for embeded systems like android.

## Syntax 

Typesets are made of two main part.
Header stores the essential things like StyleSheets etc. for the Typesetting.
On the other hand Body only carries the typeSet data.

### Header

It stores the episodes title in the specified language, some text directions and style patterns.

### Body

It stores the pure typeset data in a somehow `.ass` way. Simple syntax is like this.

`[posx;posy;styleName;textSize;textColor;Opacity]Aptal Kuze. {\fs12}èxample text{\fs}`

First brackets are mostly `override indicators and optional` but position indicators are required as you can foresee reasons.


