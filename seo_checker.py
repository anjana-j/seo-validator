import pandas as pd
from seo_functions import *
from datetime import datetime
import requests

def check_website_exists(url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.exceptions.RequestException:
            return False

class SEOChecker:
    def __init__(self, url):
        self.url = url
    def check_seo(self):
        source_code = get_source_code(self.url)

        results = {
            'Tag': [],
            'Value': []
        }

        check_google_indexing(self.url, results)

        check_title_tag(source_code, results)
        check_description_tag(source_code, results)
        check_viewport_tag(source_code, results)

        check_twitter_essential_values(source_code, results)
        check_twitter_additional_values(source_code, results)

        check_og_values(source_code, results)
        check_canonical_tag(source_code, results)
        
        #check_json_ld(source_code, results)

        check_h1_tags(source_code, results)
        check_img_alt_text(source_code, results)

        check_robots_txt(self.url, results)
        check_sitemap_xml(self.url, results)

        sitemap_xml_links(self.url, results)

        df = pd.DataFrame(results)

        print(df)

        # Generate report with dynamic file name
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        url_without_protocol = self.url.replace("https://", "")
        report_file = f"seo_report_{url_without_protocol}_{timestamp}.html"
        df.to_html(report_file, index=False, escape=False)
        print(f"SEO report generated: {report_file}")

# Test the SEOChecker class with a sample URL
connection = 'https://'
url_sender = 'absoluteadvantagefinancial.com'

url = connection + url_sender

if check_website_exists(url):
    print("Website exist.")

    seo_checker = SEOChecker(url)
    seo_checker.check_seo()
else:
    print("Website does not exist.")
