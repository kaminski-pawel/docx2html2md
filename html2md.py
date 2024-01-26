import markdownify
import re

line_beginning_re = re.compile(r"^", re.MULTILINE)


def sub_inline_conversion(markup_fn):
    """
    Returns a function that wraps the chomped text in a pair of the string
    that is returned by markup_fn. markup_fn is necessary to allow for
    references to self.strong_em_symbol etc.
    """

    def implementation(self, el, text, convert_as_inline):
        # footnotes: `el` param might be an anchor tag in a sup tag:
        # `<sup><a href="#footnote-1" id="footnote-ref-1">[1]</a></sup>`
        markup_tag = markup_fn(self)
        prefix, suffix, text = markdownify.chomp(text)
        if not text:
            return ""
        return "%s%s`%s`%s" % (prefix, markup_tag, text, suffix)

    return implementation


class MystMdConverter(markdownify.MarkdownConverter):
    class Options(markdownify.MarkdownConverter.DefaultOptions):
        heading_style = markdownify.ATX
        escape_underscores = False
        sub_symbol = "{sub}"
        sup_symbol = "{sup}"

    # TODO: use regex to find _Ref patterns and better handle making data safe

    def convert_a(self, el, text, convert_as_inline):
        prefix, suffix, text = markdownify.chomp(text)
        identif = el.get("id", "")
        href = el.get("href", "")
        if href.startswith("#footnote-") and identif.startswith("footnote-ref-"):
            return "[^%s]" % identif
        if href.startswith("#endnote-") and identif.startswith("endnote-ref-"):
            return "[^%s]" % identif
        if identif.startswith("_Ref"):
            return '<html><a id="%s">%s</a></html>' % (identif, text)
        if href.startswith("#_Ref"):
            return '<html><a href="%s">%s</a></html>' % (href, text)
        return super().convert_a(el, text, convert_as_inline)

    def convert_hn(self, n, el, text, convert_as_inline):
        if '<a href="' in text or '<a id="' in text:
            text = text.replace('<a href="', '<html><a href="')
            text = text.replace('<a id="', '<html><a id="')
            text = text.replace("</html>", "</a></html>")
        return super().convert_hn(n, el, text, convert_as_inline)

    def convert_li(self, el, text, convert_as_inline):
        identif = el.get("id", "")
        if identif.startswith("footnote-") or identif.startswith("endnote-"):
            inner = next(el.children)
            a = inner.findChild("a")
            text = inner.text.strip()
            if text.endswith(" ↑"):
                text = text[:-2]
            href = a.get("href", "")
            if href.startswith("#"):
                href = href[1:]
            return "[^%s]: %s\n" % (href, text)
        return super().convert_li(el, text, convert_as_inline)

    def convert_blockquote(self, el, text, convert_as_inline):
        if convert_as_inline:
            return text
        return "" + (line_beginning_re.sub("> ", text) + "\n") if text else ""

    convert_sub = sub_inline_conversion(lambda self: self.options["sub_symbol"])

    def convert_sup(self, el, text, convert_as_inline):
        markup_tag = self.options["sup_symbol"]
        prefix, suffix, text = markdownify.chomp(text)
        if not text:
            return ""
        if text.startswith("[^footnote-ref-"):
            return text
        if text.startswith("[^endnote-ref-"):
            return text
        return "%s%s`%s`%s" % (prefix, markup_tag, text, suffix)


def convert_to_md(soup, **options):
    # to consider: change custom options to be passed to convert_to_md(**options <==)
    return MystMdConverter(**options).convert_soup(soup)
