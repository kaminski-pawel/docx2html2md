import markdownify

# from markdownify import MarkdownConverter


# def chomp(text):
#     """
#     If the text in an inline tag like b, a, or em contains a leading or trailing
#     space, strip the string and return a space as suffix of prefix, if needed.
#     This function is used to prevent conversions like
#         <b> foo</b> => ** foo**
#     """
#     prefix = " " if text and text[0] == " " else ""
#     suffix = " " if text and text[-1] == " " else ""
#     text = text.strip()
#     return (prefix, suffix, text)


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
    # class DefaultOptions:
    #     autolinks = True
    #     bullets = '*+-'  # An iterable of bullet types.
    #     code_language = ''
    #     code_language_callback = None
    #     convert = None
    #     default_title = False
    #     escape_asterisks = True
    #     escape_underscores = True
    #     heading_style = UNDERLINED
    #     keep_inline_images_in = []
    #     newline_style = SPACES
    #     strip = None
    #     strong_em_symbol = ASTERISK
    #     sub_symbol = ''
    #     sup_symbol = ''
    #     wrap = False
    #     wrap_width = 80

    class Options(markdownify.MarkdownConverter.DefaultOptions):
        heading_style = markdownify.ATX
        sub_symbol = "{sub}"
        sup_symbol = "{sup}"

    def convert_cite(self, el, text, convert_as_inline):
        return "> " + text + "\n"

    convert_sub = sub_inline_conversion(lambda self: self.options["sub_symbol"])
    convert_sup = sub_inline_conversion(lambda self: self.options["sup_symbol"])


def convert_to_md(html, **options):
    return MystMdConverter(**options).convert(html)
