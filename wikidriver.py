import re
import lxml.etree
import urllib

def get_intro_markup(title):
    """
    Modified from http://blog.scraperwiki.com/2011/12/07/how-to-scrape-and-parse-wikipedia/
    """
    params = { "format":"xml", "action":"query", "prop":"revisions", "rvprop":"content", "rvsection":"0"}
    params["titles"] = "API|%s" % urllib.quote(title.encode("utf8"))
    qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
    url = "http://en.wikipedia.org/w/api.php?%s" % qs
    tree = lxml.etree.parse(urllib.urlopen(url))
    revs = tree.xpath('//rev')
    return revs[-1].text

def extract_links(markup_text):
    links = re.findall(r"\[\[(.*?)\]\]", markup_text)
    return links

def normalize_links(links):
    normalized_links = []
    match_files = re.compile(r"File:.*", flags=re.IGNORECASE)
    match_sublinks = re.compile(r"(.*)\|.*")
    for link in links:
        if (match_files.match(link)):
            continue
        sublink_match = match_sublinks.match(link)
        if (sublink_match):
            normalized_links.append(sublink_match.group(1))
        else:
            normalized_links.append(link)
    return normalized_links 

