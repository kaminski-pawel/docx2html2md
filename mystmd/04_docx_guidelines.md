Docx guidelines
===============

Styles
------

> <img src="media/image1.png" style="width:2.95833in;height:2.5in" alt="An example alt text." />

Figure 1. Example caption.

Cross-ref:

-   Entire caption: Figure 1. Example caption.

-   Only label and number: Figure 1

-   Only caption text: Example caption.

-   Above/below: above

-   Page number: 1

MS Word styles are your friend. There are a way for the platform to
recognize whether you intend a body of text to be a heading or a
paragraph. For a human, it may seem like an easy task in distinguishing
a paragraph from a quotation or a chapter title from a section header,
but that’s because a typical human have seen lots and lots of text and
developed an intuition in this regard. For instructions run by a
computer, this task is not so simple.

This is why you must use MS Word styles in order for the computer to
transform your manuscript into a book.

<img src="media/image2.png" style="width:6.5in;height:2.23889in" />

| \#Id      | docx-styles                                                                                                 |
|-----------|-------------------------------------------------------------------------------------------------------------|
| \#File    | ./images/docx-styles.png                                                                                    |
| \#Align   | center                                                                                                      |
| \#Caption | You can find a selection of MS Word styles in the “Home” \> “Styles” bar at the top of your MS Word window. |

Headers
-------

Use the following MS Word styles for headings in your work (e.g. for
chapter titles, section headings, subsection heading, etc.):

Heading 1 title[^1]
===================

Heading 2
---------

### Heading 3

#### Heading 4

##### Heading 5

Note that there is no heading 6.

Styling body of text
--------------------

### Paragraphs

First paragraph of each section should be styled with the “First
Paragraph” style.

Every other paragraph should be styled as the “Body Text”.

### Typography

Currently, we support the following font formatting:

*Italics.*

**Bolded text.**

Subscript (e.g. H~2~O).

Superscript (e.g. 11^th^ of November).

Note that some of the common text formatting, like <span
class="underline">underlining</span>, <s>strikethrough</s> and
highlighting are not supported and might not work.

Quotes
------

In our platform, we indicate quotations by the use of indentation.
Insert a quotation by using the “Increase Indent” button in the Home \>
Paragraph options on top of MS Word window:

Sometimes you have to put a lot of manual work to automate something.

\- Unknown Author

An alternative syntax for quotations. I wonder if the one above will
work, though. Also, is it important if we use an empty line in between.

-   Some smart quote

Horizontal Rule
---------------

To indicate section breaks in your work, you can use the horizontal
rule.

Lists
-----

<img src="media/image3.png" style="width:1.23976in;height:0.39589in" />

| \#Id   | lists-icons              |
|--------|--------------------------|
| \#File | ./images/lists-icons.png |

### Bullet lists

We support non-ordered bullet points…

-   First point
-   Second point
-   Third point

### Ordered lists (numbering)

…as well as numbered lists.

1.  First item.
2.  Second item.
3.  Third item.

### Multilevel lists

Multilevel lists are also supported.

1.  Item 1
    1.  Item 1.1
        1.  Item 1.1.1
            1.  Item 1.1.1.1
2.  Item 2

### Other lists

You can also create nested unordered lists by indenting bullet points.

-   point 1.
    -   point 1.2.
        -   point 1.3.
            -   point 1.4.
-   point 2.

Multimedia
----------

### Images

You can embed an image by linking to an image file. You can add a
caption “Insert Caption”.

Note that this will only work with tables and figures, which have titles
or captions created with the MS Word’s caption tool.

Table 1. A sample title

| Header 1        | Header 2        |
|-----------------|-----------------|
| Row 1, Column 1 | Row 1, Column 2 |
| Row 2, Column 1 | Row 2, Column 2 |

And now an image.

> <img src="media/image1.png" style="width:2.95833in;height:2.5in" alt="An example alt text." />

Figure 2. Example caption.

Write a paragraph on how to create a cross-reference. Cross-ref:

-   Entire caption: Figure 2. Example caption.

-   Only label and number: Figure 2

-   Only caption text: Example caption.

-   Above/below: above

-   Page number: 6

The same but for table:

-   Entire caption: Table 1. A sample title

-   Only label and number: Table 1

-   Only caption text: A sample title

-   Above/below: above

-   Page number: 6

Tables
------

### Simple tables

There are no explicit rules for formatting a table. As long as you will
insert a proper MS Word table, the platform should be able to recognize
it and its contents and render it.

| Header 1        | Header 2        |
|-----------------|-----------------|
| Row 1, Column 1 | Row 1, Column 2 |
| Row 2, Column 1 | Row 2, Column 2 |

Note that the styling of a table does not influence how the platform
will render it.

| Header 1        | Header 2        |
|-----------------|-----------------|
| Row 1, Column 1 | Row 1, Column 2 |
| Row 2, Column 1 | Row 2, Column 2 |

### Extended tables

We recommend describing tables with additional attribute \#Id. When
you’ll include an additional row with … By extended tables we mean
tables with additional rows that allow us to specify additional
attributes of a table. For example,

Other captions that might be helpful in a given context, include
“Caption” --- Maybe just list supported attributes

### Admonitions

Admonitions highlight a particular block of text that exists slightly
apart from the narrative of your page, such as a note or a warning.

<img src="media/image4.png" style="width:6.5in;height:1.3375in" />

| \#Id      | admonition-tip                                                |
|-----------|---------------------------------------------------------------|
| \#File    | ./images/admonition-tip.png                                   |
| \#Caption | Example of how an admonition of type \`{tip}\` can look like. |

To achieve that, you have to use the following syntax:

`:::{tip}`  
`Block of text that is separated from the rest of the page.`  
`:::`  
Aside from {tip}, you can use different admonition types, which will be
render using a color and an icon specific to that type. An icon might
change in the future, but the general principle stays the same.
Currently, the supported admonition types are as follows:

-   \`:::{tip}\`

-   \`:::{attention}\`

-   \`:::{caution}\`

-   \`:::{danger}\`

-   \`:::{error}\`

-   \`:::{hint}\`

-   \`:::{important}\`

-   \`:::{note}\`

-   \`:::{seealso}\`

-   \`:::{warning}\`

Math
----

We support MS Word equations.

$$\begin{matrix}
\nabla \times \overrightarrow{e} + \frac{\partial\overrightarrow{b}}{\partial t} & = 0 \\
\nabla \times \overrightarrow{h} - \overrightarrow{j} & = \overrightarrow{s}\_ e \\
\end{matrix}$$

$$\text{Ax} = b$$

Footnotes
---------

We support footnotes out of the box. Just insert a footnote[^2] and the
platform will handle it further.

Cross-references
----------------

### MS Word cross-reference

TODO

Admonitions

Citations
---------

### MS Word

Here we make a simple quotation (Holliday 2007). And here is an example
of more complex quotation (Holliday 2007, Perneger and Hudelson 2004).

### Zotero

Here we make a simple quotation (Frisch 1990). And here is an example of
more complex quotation (see Hall 2013, 11 for notes; Frisch 1990).

### Manual

Here we make a simple quotation \[@graves\_researcher\_1984\]. And here
is an example of more complex quotation \[e.g. @holliday\_doing\_2007,
p. 100; @perneger\_writing\_2004\].

For bibliography, go to “References” \> “Bibliography” \> “Insert
Bibliography”

Bibliography
============

Holliday, Adrian. 2007. *Doing and Writing Qualitative Research.* SAGE
Publications Ltd.Perneger, Thomas V., and Patricia M. Hudelson. 2004.
"Writing a research article: advice to beginners." *International
Journal for Quality in Health Care* 191-192.Maybe as a “**Built-in**”.
What’s the difference?

Bibliography
============

Holliday, Adrian. 2007. *Doing and Writing Qualitative Research.* SAGE
Publications Ltd.Perneger, Thomas V., and Patricia M. Hudelson. 2004.
"Writing a research article: advice to beginners." *International
Journal for Quality in Health Care* 191-192.

Or maybe there is no need for inserting a bibliography? The platform can
insert one by itself.

[^1]: Every main part of a book should open with “Heading 1”. There
    shouldn’t be more than one Heading 1 per docx file.

[^2]: To insert a footnote in MS Word, you may click the “Insert
    Footnote” button or use the “Alt + Ctrl + F” key combination.
