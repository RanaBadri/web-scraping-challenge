from splinter import Browser
from bs4 import BeautifulSoup 
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


mars_info={}

def scrape_info():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit redplanet website
    url = "https://redplanetscience.com/"
    browser.visit(url)

    #HTML object
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

#NASA Mars News
    # Scrape page into Soup
    browser.visit("https://redplanetscience.com/")
    soup = BeautifulSoup(html, "html.parser")

    #get the latest news
    news_soup = BeautifulSoup(browser.html, "html.parser")

    latest_news = news_soup.find_all("div", class_="content_title")

    latest_news=latest_news[0].text
    
    
    
    #get the paragraph under the headline above
    paragraph = news_soup.find_all("div", class_="article_teaser_body")

    paragraph=paragraph[0].text
    
    

#JPL Mars Space Images - Featured Image

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    browser.visit("https://spaceimages-mars.com/")
    import time
    time.sleep(3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image_button = browser.find_by_tag("button")[1]
    image_button.click()

    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
           
    image_pull = img_soup.find('img', class_='fancybox-image').get('src')
   
    feature_url = f'https://spaceimages-mars.com/{image_pull}'
  
    
   
#MARS FACTS
    import pandas as pd
    
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    url="https://galaxyfacts-mars.com"

    all_facts = pd.read_html(url)[1]
        
    mars_df = pd.DataFrame(all_facts)

    # Create Data Frame
    mars_df.columns = ["Description", "Value"]

    # Set index to Description
    mars_df.set_index("Description", inplace=True)
 
    html_marstable= mars_df.to_html()

    
    
#Mars Hemispheres    
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    hemi_url="https://marshemispheres.com/"
    browser.visit(hemi_url)
    time.sleep(3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')
    # Create empty list for hemisphere urls 
    hemisphere_images = []
    # Store the main_ul 
    hemispheres_main_url = "https://marshemispheres.com/"

    # Loop through the items previously stored
    for i in items: 
        # Store title
        title = i.find('h3').text
        # Store link that leads to full image website
        part_img = i.find('a', class_='itemLink product-item')['href']
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_main_url + part_img)
        # HTML Object of individual hemisphere information website 
        sub_img_html = browser.html
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = BeautifulSoup( sub_img_html, 'html.parser')
        # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        # Append the retreived information into a list of dictionaries 
        hemisphere_images.append({"title" : title, "img_url" : img_url})
    
        
    #store data in a dictionary  
    
    mars_info={
    "latest_news": latest_news,
    "paragraph": paragraph,
    "feature_url" : feature_url,
    "html_marstable": html_marstable,
    "hemisphere_images": hemisphere_images
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_info
