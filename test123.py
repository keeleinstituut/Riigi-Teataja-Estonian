# import requests
# from bs4 import BeautifulSoup
# from FileWriter_functions.writer_functions import paralyzer, subjoiner
# from FileWriter_functions.domainwriter import subcatanalyzer
# from URLcollector_functions.helper_functions import removeduplicates

# url = "https://www.riigiteataja.ee/akt/101042022010"
# no = 1
# page = requests.get(url)
# soup = BeautifulSoup(page.content, "lxml")

# bodycontent = soup.find("div", id="article-content") # body text

# for br in bodycontent.find_all("br"):
#     br.replace_with("\n")

# bodyparagraphs = bodycontent.find_all(["h1", "h2", "h3", "p"]) 
# text = "Määrus kehtestatakse"

# subcat1 = ""
# subcat2 = ""
# subcat3 = ""
# subcat4 = ""



# for paragraph in bodyparagraphs:        
#     if "Määrus kehtestatakse" in paragraph.text:
#         links = paragraph.find_all('a', href=True)
#         if links:
#             for url in links: 
#                 #print(url['href'])
#                 url = url['href']
#                 print(url)
#                 print(" ")

#                  # subcategories
#                 subcat = subcatanalyzer(url) 
#                 print(subcat)
#                 print(type(subcat))
#                 if subcat[0]:
#                     sub1 = subjoiner(subcat[0])
#                     subcat1 = ",".join([subcat1, sub1])
#                 if subcat[1]:
#                     sub2 = subjoiner(subcat[1])
#                     subcat2 = ",".join([subcat2, sub2])
#                 if subcat[2]:
#                     sub3 = subjoiner(subcat[2])
#                     subcat3 = ",".join([subcat3, sub3])
#                 if subcat[3]:
#                     sub4 = subjoiner(subcat[3])
#                     subcat4 = ",".join([subcat4, sub4])

#         else:
#             print("Ei ole")



# subcat1 = subcat1.split(",")
# subcat1 = subjoiner(subcat1)
# subcat2 = subcat2.split(",")
# subcat2 = subjoiner(subcat2)
# subcat3 = subcat3.split(",")
# subcat3 = subjoiner(subcat3)
# subcat4 = subcat4.split(",")

# print(subcat4)
# print(len(subcat4))
# subcat4 = subjoiner(subcat4)

# sub1 = 'domain_systematic="'+subcat1+'"' 
# sub2 = 'domain_Eurovoc="'+subcat2+'"' 
# sub3 = 'domain_KOV="'+subcat3+'"' 
# sub4 = 'domain_foregin="'+subcat4+'"' 

# print(sub1)
# print(sub2)
# print(sub3)
# print(sub4)


url = "./dyn=12787046&id=1045526!pr10lg1"

if url[0] == ".":
    print(len(url))
    url = "".join(["https://www.riigiteataja.ee/akt", url[1:(len(url))]])

print(url)
# results = [[], ['xyz']]

# for result in results:
#     if result:
#         print(result)
