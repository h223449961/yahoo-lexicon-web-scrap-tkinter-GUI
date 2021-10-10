# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
def buton():
    erlabel.configure(text = '',font=(24))
    global df01
    df01 = pd.DataFrame(columns=["型態",'範例'])
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',}
    sch = ''
    if myentry.get() != '':
        sch = myentry.get()
    html = requests.get(url='https://tw.dictionary.search.yahoo.com/search?p='+sch, headers=headers).content
    soup = BeautifulSoup(html,'lxml')
    try:
        nam = soup.find('span',class_='fz-24 fw-500 c-black lh-24').get_text()
        relat = soup.find_all('div',class_='pos_button fz-14 fl-l mr-12')
        expla = soup.find_all('div',class_='fz-16 fl-l dictionaryExplanation')
        excont = soup.find('div',class_='grp grp-tab-content-algo tabsContent-s tab-content-algo tabActived')
        exrelat = excont.find_all('div',class_='pos_button fz-14')
        exprela = excont.find_all('span',class_='fz-14 d-i ml-1 va-mid')
        examples = soup.find('div',class_='grp grp-tab-content-explanation tabsContent-s tab-content-explanation pt-24 tabActived')
        ples = examples.find_all('div',class_='compTitle lh-25')
        data = soup.find('ul',class_='compArticleList pt-18 pl-25 pr-25 pb-18 bg-fafafc bt-1-e5')
    except:
        erlabel.configure(text = '沒有這個字詞或資料少，只好顯示既有資訊',font=(None,24, "bold"),fg="#ff3300")
    try:
        lbox = []
        for li in data.find_all("li"):
            lbox.append(li.text)
        vex = " ".join(str(x) for x in lbox)
        typelabel.configure(text = vex,font=(None,22, "bold"))
    except:
        erlabel.configure(text = '沒有這個字詞或資料少，只好顯示既有資訊',font=(None,24, "bold"),fg="#ff3300")
    try:
        for i,j in zip(relat,expla):
            rela = i.get_text()
            epla = j.get_text()
            s01 = pd.Series([rela,epla], index=['型態','範例'])
            df01 = df01.append(s01, ignore_index=True)
            df01.index = df01.index+1
        for k,z in zip(exrelat,exprela):
            exrela = k.get_text()
            exepla = z.get_text()
            s02 = pd.Series([exrela,exepla], index=['型態','範例'])
            df01 = df01.append(s02, ignore_index=True)
            df01.index = df01.index+1
    except:
        erlabel.configure(text = '沒有這個字詞或資料少，只好顯示既有資訊',font=(None,24, "bold"),fg="#ff3300")
    exlabel.configure(text = df01.to_string(),font=(None,18))
    lst = []
    try:
        for dtg,p in zip(examples.find_all('div',class_='compTextList ml-50'),ples):
            #print(p.text)
            lst.append(p.text)
            for ultag in dtg.find_all('ul'):
                for litag in ultag.find_all('li'):
                    #print (litag.text)
                    lst.append(litag.text)
                #print('\n')
        stence = '\n'.join([ str(myelement) for myelement in lst ])
        #print (stence)
        stencelabel.configure(text = stence,font=(None,12,'bold'))
    except:
        erlabel.configure(text = '沒有這個字詞或資料少，只好顯示既有資訊',font=(None,24, "bold"),fg="#ff3300")
def main():
    global root
    root = tk.Tk()
    global myentry
    myentry = tk.Entry(root)
    myentry.pack()
    mybutton = tk.Button(root, text='查詢',font=(None,12, "bold"),fg="#eff2f3",bg='#24a0ed',command=buton)
    mybutton.pack()
    global erlabel
    erlabel = tk.Label(root, text='')
    erlabel.pack()
    global typelabel
    typelabel = tk.Label(root, text='')
    typelabel.pack()
    global exlabel
    exlabel = tk.Label(root, text='')
    exlabel.pack()
    global stencelabel
    stencelabel = tk.Label(root, text='')
    stencelabel.pack()
    root.mainloop()
if __name__ == '__main__':
    main()
