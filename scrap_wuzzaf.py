# requset to get the site url
import requests
# beautfulsoup to gather the data
from bs4 import BeautifulSoup as bf
# csv to save the data
import csv
#comment the use if the labiriry when you know it
from itertools import zip_longest


# list of columns
job_list = []
loction_list = []
company_list = []
skill_list = []
link_list =[]
responselity_list =[]
date_list = []
page_num = 0

while True :
    try:
        # url
        data = requests.get(f'https://wuzzuf.net/search/jobs/?a=hpb&q=python&start={page_num}')
        content = data.content

        # get data  fromated from link
        soup = bf(content , "lxml")
        # get the coulmns data from the formated file
        job_title = soup.find_all('h2',{"class":"css-m604qf"})
        company_name = soup.find_all('a',{"class":"css-17s97q8"})
        loction = soup.find_all('span',{"class":"css-5wys0k"})
        job_skill = soup.find_all('div',{"class":"css-y4udm8"})
        date_new =soup.find_all('div',{'class':'css-4c4ojb'})
        date_old =soup.find_all('div',{'class':'css-do6t5g'})
        date = [*date_new,*date_old]
        pagelimit = int(soup.find('strong').text)
        if (page_num > pagelimit //15):
            print('pages ended')
            break


        # get the number of row to use in the loop
        num = len(job_skill)

        # loop to extract the text
        for i in range(num):
            job_list.append(job_title[i].text)
            #try to add https// to the line to get the link work
            link_list.append(job_title[i].find('a').attrs['href'])
            company_list.append(company_name[i].text)
            loction_list.append(loction[i].text)
            skill_list.append(job_skill[i].text)
            date_text = date[i].text.replace("-","").strip()
            date_list.append(date_text)
        links_list  = ["https://wuzzuf.net" + link for link in link_list]
        page_num+=1
        print('page switched ')
        print(page_num)
    except:
        print('error occured')
# add "https://wuzzuf.net" in the link columns
file_list = [date_list,job_list ,company_list ,loction_list,skill_list,links_list]
for link in links_list:
    data = requests.get(link)
    contents_link = data.content
    soup = bf(contents_link , 'lxml')
    reqiirements = soup.find('section',{'class':"css-ghicub"}).ul
    requirement_text = ''
    #for li in reqiirements.find_all('li'):
    #     requirement_text += li.text +'| '

    responselity_list.append(requirement_text)
# apppend varible in the file list
file_list.append(responselity_list)
# export data into csv file
export = zip_longest(*file_list)
with open('/home/ahmed_elesali/project/portfilio/scraping/wuazzef_scarping/job_test.csv','w') as file:
    wr = csv.writer(file)
    wr.writerow(['date posted ','job title ','company name ','loction','skills','links','responspiltey'])
    wr.writerows(export)
