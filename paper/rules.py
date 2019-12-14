def xianzhi (url,soup):
	table = soup.find_all(class_ = 'topic-title')
	for i in range(3):
		title = table[i].string.strip()
		href = url+table[i].get('href')
		print("%-50s%10s" %(title,href))
