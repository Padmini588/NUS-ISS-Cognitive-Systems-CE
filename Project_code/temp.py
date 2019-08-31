from nltk.corpus import wordnet
synonyms = []
import xlsxwriter 
workbook = xlsxwriter.Workbook('attraction_name.xlsx') 
worksheet = workbook.add_worksheet()
row=0
col=0
dict_loc = {}
s=[]
for i in range(len(loc_dict)):
    print(i)
    a = loc_dict["name"][i]
    if a.find("(")!=-1:
        a = a.replace(a[a.index("("):],"")
    if a.find("@")!=-1:
        a = a.replace(a[a.index("@"):],"")    
    if a not in s and a!='':
        s.append(a.strip())

dict_loc["location"] = s
dict_loc=pd.DataFrame(dict_loc)
dict_loc.to_csv("locations.csv")





worksheet.write(row, col, "attraction_name")
for x in s:
    col += 1
    for syn in wordnet.synsets(tags[x]):
        for l in syn.lemmas():
            synonyms.append(l.name())
    for y in synonyms:
     worksheet.write(row, col, y)
     col += 1
    row += 1
    synonyms.clear()
    
    
workbook.close()