import json
import requests
from bs4 import BeautifulSoup

def get_source_code(url):
    # Retrieve the source code
    response = requests.get(url)
    return response.text


def check_google_indexing(url, results):
    url_without_protocol = url.replace("https://", "")
    search_url = f"https://www.google.com/search?q=site:{url_without_protocol}"

    response = requests.get(search_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = soup.find_all("div", class_="DnJfK")

        if len(search_results) > 2:
            results['Tag'].append('Google Indexing')
            results['Value'].append('Indexed')
            return
    results['Tag'].append('Google Indexing')
    results['Value'].append('Not Indexed')


def check_title_tag(source_code, results):
    # Parse the HTML content
    soup = BeautifulSoup(source_code, 'html.parser')

    # Find the title tag
    title_tag = soup.find('title')

    if title_tag:
        # Extract the text inside the title tag
        title_text = title_tag.text.strip()
        title_length = len(title_text)
        results['Tag'].append('Title')
        results['Value'].append("{} ({})".format(title_text, title_length))

def check_description_tag(source_code, results):
    # Parse the HTML content
    soup = BeautifulSoup(source_code, 'html.parser')

    # Find the meta description tag
    description_tag = soup.find('meta', attrs={'name': 'description'})

    if description_tag:
        # Extract the text inside the description tag
        description_text = description_tag['content'].strip()
        description_length = len(description_text)
        results['Tag'].append('Description')
        results['Value'].append("{} ({})".format(description_text, description_length))


def check_viewport_tag(source_code, results):
    # Parse the HTML content
    soup = BeautifulSoup(source_code, 'html.parser')

    # Find the viewport tag
    viewport_tag = soup.find('meta', attrs={'name': 'viewport'})

    if viewport_tag:
        # Check if the required content value exists
        viewport_content = viewport_tag['content']
        if "width=device-width, initial-scale=1" in viewport_content:
            results['Tag'].append('Viewport')
            results['Value'].append(viewport_content)
        else:
            results['Tag'].append('Viewport')
            results['Value'].append(viewport_content)

def check_twitter_essential_values(source_code, results):
    # Parse the HTML content
    soup = BeautifulSoup(source_code, 'html.parser')

    # Twitter essential values
    essential_tags = ['twitter:card', 'twitter:title', 'twitter:description', 'twitter:image']

    for tag in essential_tags:
        meta_tag = soup.find('meta', attrs={'name': tag}) or soup.find('meta', attrs={'property': tag})
        if meta_tag:
            content_value = meta_tag.get('content', '')
            results['Tag'].append(tag)
            results['Value'].append(content_value)
        else:
            results['Tag'].append(tag)
            results['Value'].append(None)

def check_twitter_additional_values(source_code, results):
    # Parse the HTML content
    soup = BeautifulSoup(source_code, 'html.parser')

    # Twitter additional values
    additional_tags = ['twitter:site', 'twitter:creator', 'twitter:url']

    for tag in additional_tags:
        meta_tag = soup.find('meta', attrs={'name': tag}) or soup.find('meta', attrs={'property': tag})
        if meta_tag:
            content_value = meta_tag.get('content', '')
            results['Tag'].append(tag)
            results['Value'].append(content_value)
        else:
            results['Tag'].append(tag)
            results['Value'].append(None)

def check_og_values(source_code, results):
    # Parse the HTML content
    soup = BeautifulSoup(source_code, 'html.parser')

    # Open Graph values
    og_tags = ['og:title', 'og:type', 'og:url', 'og:image', 'og:description', 'og:site_name', 'og:locale']

    for tag in og_tags:
        meta_tag = soup.find('meta', attrs={'property': tag})
        if meta_tag:
            content_value = meta_tag.get('content', '')
            results['Tag'].append(tag)
            results['Value'].append(content_value)
        else:
            results['Tag'].append(tag)
            results['Value'].append(None)

def check_canonical_tag(source_code, results):
    # Parse the HTML content
    soup = BeautifulSoup(source_code, 'html.parser')

    # Find the canonical tag
    canonical_tag = soup.find('link', attrs={'rel': 'canonical'})

    if canonical_tag:
        # Extract the value of the href attribute
        canonical_url = canonical_tag.get('href', '')
        results['Tag'].append('Canonical')
        results['Value'].append(canonical_url)
    else:
        results['Tag'].append('Canonical')
        results['Value'].append(None)


def check_json_ld(source_code, results):
    # Parse the HTML content
    soup = BeautifulSoup(source_code, 'html.parser')

    # Find the JSON-LD script tag
    script_tag = soup.find('script', attrs={'type': 'application/ld+json'})

    if script_tag:
        # Extract the JSON-LD content
        json_ld_content = script_tag.string

        try:
            # Parse the JSON content
            json_data = json.loads(json_ld_content)

            for key, value in json_data.items():
                results['Tag'].append(key)
                results['Value'].append(value)

        except json.JSONDecodeError:
            results['Tag'].append('JSON-LD')
            results['Value'].append('Invalid JSON-LD content.')

    else:
        results['Tag'].append('JSON-LD')
        results['Value'].append(None)


def check_h1_tags(source_code, results):
    # Parse the HTML content
    soup = BeautifulSoup(source_code, 'html.parser')

    # Find all the h1 tags
    h1_tags = soup.find_all('h1')

    if len(h1_tags) == 0:
        results['Tag'].append('Total H1 tags')
        results['Value'].append('0')
    else:
        results['Tag'].append('Total H1 tags')
        results['Value'].append(str(len(h1_tags)))

        for index, h1_tag in enumerate(h1_tags):
            h1_value = h1_tag.get_text()
            results['Tag'].append('H1 {}'.format(index + 1))
            results['Value'].append(h1_value)

        if len(h1_tags) > 1:
            results['Tag'].append('H1 Caution')
            results['Value'].append('Multiple H1 tags found.')



def check_img_alt_text(source_code, results):
    # Parse the HTML content
    soup = BeautifulSoup(source_code, 'html.parser')

    # Find all the img tags
    img_tags = soup.find_all('img')

    if len(img_tags) == 0:
        results['Tag'].append('IMG')
        results['Value'].append(None)
    else:
        results['Tag'].append('IMG')
        results['Value'].append(str(len(img_tags)))

        for index, img_tag in enumerate(img_tags):
            alt_text = img_tag.get('alt', '')
            src = img_tag.get('src', '')
            value = f"src: {src}<br>alt: {alt_text}"
            results['Tag'].append('IMG {}'.format(index + 1))
            results['Value'].append(value)

def check_robots_txt(url, results):
    # Construct the robots.txt URL
    robots_url = url.rstrip('/') + '/robots.txt'

    # Send a GET request to the robots.txt URL
    response = requests.get(robots_url)

    if response.status_code == 200:
        robots_txt = response.text.replace('\n', '<br>')
        results['Tag'].append('Robots.txt')
        results['Value'].append(robots_txt)
    else:
        results['Tag'].append('Robots.txt')
        results['Value'].append(None)



def sitemap_xml_links(url, results):
    # Construct the sitemap.xml URL
    sitemap_url = url.rstrip('/') + '/sitemap.xml'

    # Send a HEAD request to the sitemap.xml URL
    response = requests.head(sitemap_url)

    if response.status_code == 200:
        results['Tag'].append('Sitemap.xml')

        # Get the XML content of the sitemap
        sitemap_response = requests.get(sitemap_url)
        if sitemap_response.status_code == 200:
            # Parse the sitemap XML content
            soup = BeautifulSoup(sitemap_response.content, 'xml')

            # Find all the loc tags
            loc_tags = soup.find_all('loc')

            if len(loc_tags) > 0:
                # Extract the values inside loc tags
                loc_values = [loc.text for loc in loc_tags]

                # Join the loc values with <br> tags
                loc_values_with_br = '<br>'.join(loc_values)

                # Append the loc values to the results
                results['Value'].append(loc_values_with_br)
            else:
                results['Value'].append(None)
        else:
            results['Value'].append(None)
    else:
        results['Tag'].append('Sitemap.xml Links')
        results['Value'].append(None)

def check_sitemap_xml(url, results):
    # Construct the sitemap.xml URL
    sitemap_url = url.rstrip('/') + '/sitemap.xml'

    # Send a HEAD request to the sitemap.xml URL
    response = requests.head(sitemap_url)

    if response.status_code == 200:
        results['Tag'].append('Sitemap.xml')

        # Get the XML content of the sitemap
        sitemap_response = requests.get(sitemap_url)
        if sitemap_response.status_code == 200:
            # Parse the sitemap XML content
            soup = BeautifulSoup(sitemap_response.content, 'xml')

            # Find all the loc tags
            loc_tags = soup.find_all('loc')

            if len(loc_tags) > 0:
                # Count the number of loc tags
                num_links = len(loc_tags)

                # Append the number of links to the results
                results['Value'].append(f"Number of Links: {num_links}")
            else:
                results['Value'].append(None)
        else:
            results['Value'].append(None)
    else:
        results['Tag'].append('Sitemap.xml')
        results['Value'].append(None)
