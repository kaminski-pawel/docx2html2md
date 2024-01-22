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

    def convert_blockquote(self, el, text, convert_as_inline):
        if convert_as_inline:
            return text
        return "" + (line_beginning_re.sub("> ", text) + "\n") if text else ""

    convert_sub = sub_inline_conversion(lambda self: self.options["sub_symbol"])
    convert_sup = sub_inline_conversion(lambda self: self.options["sup_symbol"])


def convert_to_md(soup, **options):
    # to consider: change custom options to be passed to convert_to_md(**options <==)
    return MystMdConverter(**options).convert_soup(soup)
