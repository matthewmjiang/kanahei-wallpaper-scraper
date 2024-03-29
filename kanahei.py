from selenium import webdriver
import requests

driver = webdriver.Chrome("/mnt/c/VSCode/chromedriver/chromedriver.exe")
driver.get("http://www.kanahei.com/kabegami/")

# list to store all wallpaper links
links = []

# start from page 1
page = 1
while page <= 10:
    #print("on page " + str(page))
    # find all link elements with the text '1920x1200'
    link_elements = driver.find_elements_by_link_text('1920×1200')

    # if we're still on the first page..
    if driver.current_url == "http://www.kanahei.com/kabegami/":
        # also find all link elements with the text '16:9' since only the
        # first page has these.
        link_elements += driver.find_elements_by_link_text('16:9')

    # loop through the link elements
    for element in link_elements:
        # add the urls of each link element to the links list
        links.append(element.get_attribute('href'))
        #print(element.get_attribute('href'))

    # go to the next page while page is not already at 10
    if page != 10:
        next_page_elem = driver.find_element_by_link_text(str(page+1))
        driver.get(next_page_elem.get_attribute('href'))
    else:
        # quit if we're at page 10
        driver.quit()
    
    page += 1


# enumerate adds the count next to each element in the links list.
# i.e ['wallpaper1', 'wallpaper2'] = [(1, 'wallpaper1'), (2, 'wallpaper2')]
for count, link in enumerate(links, start=1):
    #print(link)
    r = requests.get(link)

    # open a new file in the kanahei-wallpapers directory with a name determined by the count.
    # zfill just pads the number with zeros.
    # wb mode is write bytes
    # write the picture (r.content) to the file using f.write.
    with open(('kanahei-wallpapers/' + str(count).zfill(3) + '.jpg'), 'wb') as f:
        f.write(r.content)

