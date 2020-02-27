HEY YOU!

Make this a collection of unix pipe things.

article =

  $ removeComments | process indents | newline sections | frame | decodeFrames | renderHTML

Two choices:

- Get into internal data models right away
- Stay in line-delinated text as long as possible.

I think option 2 is where I'm headed.

0. The Art of Articles

  I want to build another markdown for my own personal use. Some of you out there may feel that this is irresponsible. Nevertheless, I'm going to press forward. There will be things here that are simply impossible. That's OK because you can always go in and manually edit the generated HTML or whatever. Honestly, that's not such a bad tradeoff.

  This is a line-based format, which means processing will happen line by line. You cannot begin a link on one line and end it on another.

  Separation between things is generally signified by 3 newline characters in a row. Visually, this looks like there are two blank lines between separate

  --

  A horizontal Ruler just happened above. Cool, huh?




1. Metadata

  Each article begins with metadata. It must have at least one piece of metadata. Like maybe "title" or "author.email". Something.

  It's written key value pairs in the form of "key: value\n" where "key" is basically anything up until the first colon on the line, and "value" is everything after the two characters ": ". Yep, you can throw '\n' into your value, but it's not going to be interpreted the way you expect. It will just appear as a raw slash followed by n.

  Metadata is separated from the body of the document by three newlines.


2. Headings

  A heading is a single line of text separated three newlines above and one newline below. If headings begin as the first bit of text on a line, they are consitered to be at the H1 level. Subheadings can be achieved in two different ways.

  First, The parent heading can be prepended to the subheading, separated by " : ". So if the parent heading was "Animals With Paws", the subheading would be "Animals With Paws : Cats" and renders as an H2 title. Note that the space must be there. For flexibility, the heading "Animals with Paws: Cats" (which differs only by one space) would be treated as an H1 heading.

  Second, the entire first section may be omitted. Using the example from above, the second title would then be written as ": Cats" and would act the same.

  Both of these methods stacks, so both ":: Calico" and "Animals With Paws : Cats : Calico" are equivalent and would be rendered as H3.


3. Body & Paragraphs

  There's no body here. But tha's okay, it's just weird visually.


4. Links

  Links may be added by surrounding the linked text with less than/greater than operators. For instance: This bit <here is a link:http://www.google.com> to google.com.

  Links can point to several things: URLs, sections, footnotes, and inline notes.

  - This is a |link:N3| to inline note number 3.

  - This is a |link:F4| to footnote number 4.

  - This is a |link:F| to the footnote that appears next in the document

  - This is relative |in:/img/panda.jpg| to a an image of a panda.

  - This is a |link:S4| to the section on links.

  - This is a <link:Quotes, Code, Preformatted Text> to the section just below this one. However, this link calls it out by name.ddd

    footnote:
    This is one of them. Yep. That's what the link above will link to.

    footnote:
    This is another footnote. By the way, notice how this had to be separated from the previous footnote by three consecutive newlines.

  Finally, if you make something obvious a link that the engine can figure out, it'll do the right thing for you. For example, if you say this is <http://www.google.com> well, I mean that's pretty straighforward. But you can also use any of the section headings. If the footnote IDs


4. Quotes, Code, Preformatted Text

  In an effort to keep things as simple as possible, both quotes and code share kind of the same format. They are both double-indented, but code begins with a line that says "code: <language>"  or "quote:". Another option is available for preformatted text, which is just "text:". Here's some examples:

    code: bash
    #!/bin/bash

    echo "This is a shell script!"
    echo "How do you know when the quote is supposed to stop?"


    code: node.js

  When the indendtation returns to normal or there's three new lines. Here's another example:

    quote:
    It is a tale told by an idiot
    full of sound and fury
    signifying nothing.

  And finally, ascii art:

    text:
    Name    | Phone        |

    --------+--------------+
    Jonh    | 555-555-5555 |
    Jacob   | 666-666-6666 |


5. Footnotes & Inline Notes

  For those of you who are fans of D.F. Wallace, footnotes and inline notes, would it? Of course not. They follow roughly the same convention as earlier - double-indented paragraphs with a little hint at the start so the parser (and actually reader) knows how to interpret it. For footnotes, mark as "footnote: N", where N is just whatever number it is. Hell, N can be a string. For inline notes, make a link to an inline either by ID or by "assumed ID" |N:|, which just means "the next inline note in the document".

    note:
    Like the footnotes, an unnamed inline note just means


What do I do about comments?