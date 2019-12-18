def xianzhi (url,soup):
	table = soup.find_all(class_ = 'topic-title')
	for i in range(3):
		title = table[i].string.strip()
		href = url+table[i].get('href').strip()
		print("%-40s%s" %(title,href))
