
from bs4 import BeautifulSoup
import requests
import sys

a = Stockholm
# desktop user-agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"

headers = {"user-agent": USER_AGENT}
r = requests.get("https://www.foodora.se/en/city/stockholm?r=1", headers=headers)

print("Status code: ", r.status_code)

if r.status_code == 200:
    # resp = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
else:
    print("Code is not valid")
    sys.exit(0)

# finds each product from the store page
containers = soup.find("div", {"class": "main-content restaurants-container"})

container = containers.find_all("li")

# name the output file to write to local disk
out_filename = "foodora.csv"
# header of csv file to be written
headers = "Restaurant,Rating \n"

# opens file, and writes headers
f = open(out_filename, "w+")
f.write(headers)

# loops over each product and grabs attributes about
# each product
for con in container:

    anchors = con.find_all('span', {"class": "headline"})
    if anchors:

        rating = con.find("span", {"class" : "rating--label-primary cl-rating-tag-text f-label-small-font-size fw-label-small-font-weight lh-label-small-line-height"})
        title = con.find('a', {"class" : "name fn"})

        if rating is None:
            c = title.text
            b= None
        else:
            #b = rating.strong.text.encode('utf-8')
            b = rating.text
            c = title.text

        # prints the dataset to console
        print(c)
        print(b)
        print(c, b, file=open(out_filename, "a"))


f.close()  # Close the file

