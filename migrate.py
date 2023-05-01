from bs4 import BeautifulSoup
import re



sections = ['HOME', 'SPONSORS', 'DONATIONS', 'SCHOLARSHIP/GRANT', 'PHOTOS', 'CONTACT US']
section_orders = [1, 2, 4, 5, 6]
make_id = lambda x: 'SITE_FOOTER' if x == 'CONTACT US' else re.sub('[/ ]','-',x).lower()

with open("contents.html", encoding='utf-8') as fp:
    soup = BeautifulSoup(fp, 'html.parser')

    soup.find(id="WIX_ADS").string=''
    for elem in soup(text=re.compile('HOME.*SPONSORS', re.MULTILINE|re.DOTALL)):
        #print(elem.parent)
        navbar = elem.parent
        navbar.string = ''
        for section in sections:
            new_link = soup.new_tag('a', href='#'+make_id(section))
            new_link.string = section
            new_link['class'] = 'underline-on-hover'
            navbar.append(new_link)
            navbar.append('\xa0\xa0\xa0\xa0\xa0')
    section_container = soup.findAll('div', {"data-mesh-id": "Containerc1dmpinlineContent-gridContainer"})[0]
    section_divs = section_container.findChildren("section", recursive=False)
    
    section_divs[1].findChildren("div", {"data-testid": "inline-content"})[0]["id"] = make_id(sections[0])
    section_divs[2].findChildren("div", {"data-testid": "inline-content"})[0]["id"] = make_id(sections[1])
    section_divs[4].findChildren("div", {"data-testid": "inline-content"})[0]["id"] = make_id(sections[2])
    section_divs[5].findChildren("div", {"data-testid": "inline-content"})[0]["id"] = make_id(sections[3])
    section_divs[6].findChildren("div", {"data-testid": "inline-content"})[0]["id"] = make_id(sections[4])
    

    styles = soup.find(id="css_masterPage")
    styles.append("html{scroll-behavior: smooth;}")
    styles.append(".underline-on-hover:hover {text-decoration: underline;}")
    styles.append("#site-root{top:0;}")

    for icon_link in soup.findAll('link', {"href": "https://www.wix.com/favicon.ico"}):
        icon_link["href"] = "./assets/ccf-logo-icon.ico"

    with open("index.html", "w", encoding='utf-8') as fout:
        fout.write(str(soup))
        
