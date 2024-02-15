import re
import bs4
import typing as t
from md_extraction import AssetMetadata, BookMetadata


def replace_assets_with_directives(
    html_soup: bs4.BeautifulSoup, metadata: BookMetadata
) -> bs4.BeautifulSoup:
    for table in html_soup.find_all(["table"]):
        if "##" in table.text:
            asset_meta = AssetMetadata()
            key, val = "", ""
            for tr in table.find_all(["tr"]):
                for descendent in tr.find_all():
                    if re.match(r"^\s*##\s*\w+", descendent.text):
                        key = descendent.text
                    else:
                        val = descendent.text
                if key:
                    asset_meta.add(key, val)
            if asset_meta:
                metadata.add_asset_metadata(asset_meta)
                prev_el = table.previous_sibling
                # comment = bs4.Comment("% :::{dgt-mon-asset} " + asset_meta.uuid)
                # table.replace_with(comment)
                p = html_soup.new_tag("p")
                p.string = "\n% :::{dgt-mon-asset} " + asset_meta.uuid
                table.replace_with(p)
                if asset_meta.delete_prev and asset_meta.digital_fp:
                    prev_el.extract()
    return html_soup
