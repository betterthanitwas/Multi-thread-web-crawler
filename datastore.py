import mysql.connector

class DataStore:
	# connect to db
	def __init__(self, h, db, u, pwd):
		self.host = h
		self.database = db
		self.user = u
		self.password = pwd
		# create connection
		self.conn = mysql.connector.connect(host= self.host,database=self.database,user=self.user,password=self.password)
		# create a cursor to call procedures
		self.cursor = self.conn.cursor()

	# (url, title, Dict<word, (wordCount, excerpt)>) -> Int
	def indexPage(self, url, title, words):
		""" Inputs are a url (string), title (string), Dict<word (string), tuple(wordCount (int), excerpt(string)>
			Returns 0 if no problem, 1 if error storing info, 2 if database is not connected
		"""
		# check connection
		if conn.is_connected():			
			
			# maybe start transaction? - no, not as a single user db
			try:
				# check lengths: URL <= 255 title <= 100 
				url = url[0:255]
				title = title[0:100]

				# store url & title 
				args = [url, title]
				self.cursor.callproc('PRC_STORE_URL_TTL', args)

				''' NEXT VERSION HAVE MYSQL ITERATE THROUGH LIST OF WORDS '''

				# store word, wordcount and excerpt
				for word, wordData in words:

					# check lengths: Word <= 45, excerpt <= 150
					count = (wordData[0])[0:45]
					excerpt = (wordData[1])[0:150]

					# store word id, word, word count and excerpt into db
					args = [word, wordData[0], wordData[1]]
					self.cursor.callproc('PRC_STORE_WRD', args)

				# call commit
				conn.commit()

				return 0

			except Error(e):
				return 1
		else:
			return 2
			
			
	# List<word> -> List<(url, title, excerpt)>
	def search(self, words):
		""" Inputs are a list of words
			Returns list of sets if no problem, 
			1 if error storing info, 
			2 if database is not connected
		"""
		# check connection
		if conn.is_connected():			
			
			retList = []

			try:

				for word in words:
					# find word in database and return a row
					# pass list of words to database
					args[word]
					self.cursor.callproc('PRC_FIND_WORD', args)

					# add result to return list 
					for result in cursor.stored_results():
						print(result.fetchall())
						#retList.append(result)

				''' DO THIS SECOND
				# pass list of words to database
				args[words]
				self.cursor.callproc('PRC_FIND_WORD', args)

				# add result to return list 
				for result in cursor.stored_results():
					print(result.fetchall())
					#retList.append(result)
				'''
				return retList

			except Error(e):
				return list(1)
		else:
			return list(2)

		
	def closeConnection(self):
		self.cursor.close()
		self.conn.close()

def main():
	ds = DataStore('localhost', 'webcrawl', 'root', '')
	ds.closeConnection()

if __name__ == "__main__":
	main()