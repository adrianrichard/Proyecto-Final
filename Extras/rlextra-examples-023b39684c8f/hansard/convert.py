"""Script to convert a Hansard URL to a PDF document"""
import argparse
import json
import os
import preppy
import re
import bs4


from bs4 import BeautifulSoup
from io import BytesIO
from pprint import pprint
from rlextra.rml2pdf import rml2pdf
from reportlab.lib.utils import asBytes


EXAMPLE_SESSION_URL = "https://hansard.parliament.uk/Commons/2024-05-02/debates/F7540B05-869A-40BD-9374-02F1D32A4BF7/SecurityInTheWesternBalkans"


def validate_url(url):
    date_regex = r'd{4}-\d{2}-\d{2}'
    uuid_regex = '[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}'
    url_regex = fr'^https:\/\/hansard.parliament.uk\/(Commons|Lords)\/\{date_regex}\/debates\/{uuid_regex}\/[a-zA-Z]*$'
    pattern = re.compile(url_regex)
    matches = pattern.match(url)
    if not matches:
        raise ValueError("Url does not follow the correct structure")


def get_title_from_url(url):
    """Check if url is in the correct format and if so the title should be at the end"""
    validate_url(url)
    return url.split("/")[-1]


def selenium_fetch_html_page(url):
    title = get_title_from_url(url)
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    options = Options()
    options.add_argument("-headless")
    with webdriver.Firefox(options=options) as driver:
        driver.get(url)
        page_source = driver.page_source
    filepath = os.path.join('data', f'{title}.html')
    with open(filepath, 'w') as _:
        _.write(page_source)
    return filepath


def strip_invalid_tags(para):
    """There are a variety of bad tags, many starting with "column-number", "sr-only" is a standalone bad tag.
    # We must strip this content"""
    if not para:
        return para

    for tag in para.findChildren():
        attrs = getattr(tag, 'attrs', {})
        if attrs:
            classes = attrs.get('class', [])
            if classes:
                for class_name in classes:
                    if class_name.startswith("column-number"):
                        tag.decompose()


def create_pdf(debate):
    """Creates PDF as a binary stream in memory, and returns it

    This can then be used to write to disk from management commands or crons,
    or returned to caller via Django views.
    """
    RML_DIR = 'rml'
    templateName = os.path.join(RML_DIR, 'hansard_template.prep')
    template = preppy.getModule(templateName)
    namespace = {
        'debate':debate,
        'RML_DIR': RML_DIR,
        'IMG_DIR': 'img'

        }
    rml = template.getOutput(namespace,quoteFunc=preppy.stdQuote)
    # open(os.path.join(DATA_DIR,'latest.rml'), 'wb').write(asBytes(rml))
    buf = BytesIO()
    rml2pdf.go(asBytes(rml), outputFileName=buf)
    return buf.getvalue()


def run(url, filepath):
    html = open(filepath).read()
    lord_or_commons = url.replace("https://", "").replace("http://", "").split("/")[1]
    soup = BeautifulSoup(html, 'html.parser')
    debate = soup.find('main', id='main-content')
    title = debate.find("h1").get_text().strip()
    subtitle = debate.find("h2").get_text().strip()

    breadcrumbs = soup.find('div', class_='breadcrumb')
    bcs = []
    if breadcrumbs:
        for c in breadcrumbs.find_all("a"):
            href = c.attrs['href']
            if href.startswith("/"):
                href = "https://hansard.parliament.uk" + href
            bcs.append({"title": c.get_text().strip(), "href": href})

    contribs = debate.find_all("div", class_="debate-item")
    print("found %d contributions" % len(contribs))

    parsed = []
    for contrib in contribs:
        # A debate item will be one of:
        #   * Timestamp
        #   * Speaker + Contribution (same block initially unless interrupted)
        #   * Other contribution (interrupted contribution or standalone text)

        info = {}
        info["content"] = content = []

        # Time based debate items
        time = contrib.find("time")
        if time:
            info['time'] = time.get_text().strip()
            parsed.append(info)
            continue

        # Both speaker and the contribution would be grouped together here
        primary = contrib.find("div", class_="primary-text")
        # TODO: There is a problem with duplicating speakers. And the logic is inconsistent,
        #  see WaterCompaniesFailure for a demonstration with Baroness Jones and Lord Douglas-Miller
        if primary:
            speaker = primary.get_text().strip()
            secondary = contrib.find("div", class_="secondary-text")
            if secondary:
                suffix = secondary.get_text().strip()
                speaker += " " + suffix
            info["speaker"] = speaker

            for cont_item in contrib.find_all("div", class_="content"):
                paras = cont_item.find_all("p")
                for para in paras:
                    strip_invalid_tags(para)
                    text = para.get_text().strip()
                    if text:
                        content.append({"text": text, "italics": bool(para.find("em"))})

        else:
            # Contributions that get interrupted by other debate items
            div = contrib.find("div")
            if div:
                # No non-singular examples found
                para = div.find("p")
                strip_invalid_tags(para)
                text = para.get_text().strip()
                if text:
                    content.append({"text": text, "italics": bool(para.find("em"))})

        if content:  # empties occur
            parsed.append(info)

    outer = dict(title=title, subtitle=subtitle, source=url, house=lord_or_commons)
    outer["contributions"] = parsed
    outer["breadcrumbs"] = bcs

    json_file_name = os.path.splitext(filepath)[0] + ".json"
    f = open(json_file_name, "w")
    f.write(json.dumps(outer, indent=2))
    print("wrote", json_file_name)

    pdf = create_pdf(outer)

    pdf_file_name = os.path.splitext(filepath)[0] + ".pdf"
    open(pdf_file_name,'wb').write(pdf)
    print('Created %s' % pdf_file_name)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument("--url", help="url of the hansard page")
    args = parser.parse_args()
    url = args.url or EXAMPLE_SESSION_URL
    print(f"Hansard url: {url}")
    filepath = selenium_fetch_html_page(url)
    run(url=url, filepath=filepath)

