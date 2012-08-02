import re
import lxml.etree
import urllib
from relatedness import Semantic_Network

def get_intro_markup(title):
    """ Returns all of the MediaWiki markup text in the introduction section of the article with the specifed title.
    Modified from http://blog.scraperwiki.com/2011/12/07/how-to-scrape-and-parse-wikipedia/
    """
    params = { "format":"xml", "action":"query", "prop":"revisions", 
                "rvprop":"content", "rvsection":"0"}
    params["titles"] = "API|%s" % urllib.quote(title.encode("utf8"))
    qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
    url = "http://en.wikipedia.org/w/api.php?%s" % qs
    tree = lxml.etree.parse(urllib.urlopen(url))
    revs = tree.xpath('//rev')
    return revs[-1].text

def extract_links(markup_text):
    """ Returns a list of all of the WikiMedia-internal links in the specified markup text.
    """
    links = re.findall(r"\[\[(.*?)\]\]", markup_text)
    return links

def normalize_links(links):
    """ Returns a list of usable links from the list of links provided.

    Removes all file and image links from the list. If a link in the list specifies a specific section of another article, this function will replace it with a link to the greater article linked to. For example, "United States Presidents | Thomas Jefferson" would become "United States Presidents"
    """
    normalized_links = []
    match_files = re.compile(r"File:.*", flags=re.IGNORECASE)
    match_images = re.compile(r"Image:.*", flags=re.IGNORECASE)
    match_sublinks = re.compile("(.*)[\|#].*")
    for link in links:
        if (match_files.match(link)):
            continue
        if (match_images.match(link)):
            continue
        sublink_match = match_sublinks.match(link)
        if (sublink_match):
            normalized_links.append(sublink_match.group(1))
        else:
            normalized_links.append(link)
    return normalized_links 

def extract_normalized_links(article_title):
    """ Returns a normalized list of all the links in the introduction section of the specified article.
    """
    return normalize_links(extract_links(get_intro_markup(article_title)))

def build_network(base_article, depth=3, strength=50):
    """ Returns a semantic network centered on the Wikipedia article with title base_article, and containing all articles within depth links of the base_article.

    The Semantic_Network returned will contain the base_article, which will be connected to each of the articles linked to by the intro paragraph. Each of those articles will be connected to all on the articles in their intro paragraphs. This continues for depth iterations.
    """
    network = Semantic_Network()
    queue = [base_article]
    next_queue = []
    for level in range(depth):
        for article in queue:
            for link in extract_normalized_links(article):
                network.connect(article, link, strength)
                if level != depth - 1:
                    next_queue.append(link)
        queue = next_queue
        next_queue = []
    return network

