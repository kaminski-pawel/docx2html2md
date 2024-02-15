import markdownify
import re

from md_extraction import BookMetadata, AssetDatapoint, AssetMetadata

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

    def __init__(self, metadata: BookMetadata, **options):
        self._metadata = metadata
        super().__init__(**options)

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

    def convert_p(self, el, text, convert_as_inline):
        re_match = re.match(r"\s*%\s*:::{dgt-mon-asset}\s*", text)
        if re_match is not None:
            uuidv4_len = 36
            uuid = text[re_match.span()[1] :][:uuidv4_len]
            asset_meta = self._metadata[uuid]
            if asset_meta.digital_fp.suffix == ".html":
                text = (
                    "<html>"
                    f'<iframe src="{str(asset_meta.digital_fp)}">'
                    "</iframe>"
                    "</html>"
                )
        elif text.startswith(
            ":::{iframe} <https://www.youtube.com/embed/"
        ) or text.startswith(":::{iframe} <https://player.vimeo.com/video/"):
            text = text.replace("<", "", 1)
            text = text.replace(">", "", 1)
        return super().convert_p(el, text, convert_as_inline)

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

    # def convert_table(self, el, text, convert_as_inline):
    #     if "##" in text:
    #         asset_meta = AssetMetadata()
    #         key, val = "", ""
    #         for tr in el.find_all(["tr"]):
    #             for descendent in tr.find_all():
    #                 if re.match(r"^\s*##\s*\w+", descendent.text):
    #                     key = descendent.text
    #                 else:
    #                     val = descendent.text
    #             if key:
    #                 asset_meta.add(key, val)
    #         if asset_meta:
    #             self._metadata.add_asset_metadata(asset_meta)
    #             return "\n% :::{dgt-mon-asset} " + asset_meta.uuid + "\n"
    #         return "\n"
    #     return super().convert_table(el, text, convert_as_inline)


# class PostProcessor:
#     def __init__(self, metadata: BookMetadata, **options):
#         self._metadata = metadata
#         self._options = options

#     def enact_directives(self, md: str) -> str:
#         """
#         Iterate in reverse order on each markdown line and
#         act on internal directives.
#         """
#         result = ""
#         newline_count = 0
#         # remove_next_obj = False
#         current_block = ""
#         uuidv4_len = 36
#         lines = md.split("\n")
#         # for line in md.split("\n")[::-1]:
#         for i in range(len(lines) - 1, -1, -1):
#             prevline = lines[i + 1] if i + 1 < len(lines) else ""
#             line = lines[i]
#             nextline = lines[i - 1] if i - 1 >= 0 else ""
#             current_block = line + "\n" + current_block if current_block else line
#             # if line.startswith("% :::{dgt-mon-asset} "):
#             # remove_next_obj = True
#             re_match = re.match(r"%\s*:::{dgt-mon-asset}\s*", line)
#             if re_match is not None:
#                 uuid = line[re_match.span()[1] :][:uuidv4_len]
#                 asset_meta = self._metadata[uuid]
#                 if asset_meta.delete_prev:
#                     current_block = ""
#                     current_block += line + "\nREMOVE PREVIOUS BLOCK!!!"
#             elif line == "" and prevline != "":  # and remove_next_obj == False:
#                 result = current_block + "\n" + result
#                 current_block = ""
#             elif line == "":
#                 result = "\n" + result
#         result = current_block + "\n" + result
#         return result


def convert_to_md(soup, metadata: BookMetadata, **options) -> str:
    # TODO: change custom options to be passed to convert_to_md(**options <==)
    return MystMdConverter(metadata, **options).convert_soup(soup)
