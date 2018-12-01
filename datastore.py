import mysql.connector
from mysql.connector import errorcode
from python_mysql_dbconfig import read_db_config
import threading

class DataStore:
	def __init__(self, configFile):
		'''
		Example:
			ds = DataStore('config.ini')
			ds.connect()

			url = 'www.Thisisatest.com'
			title = 'Test Title'
			dictWord = {'test1': (50, "this test1 word is a test excerpt"),
						'test2': (10, "this test2 : excerpt")}
			ds.indexPage(url, title, dictWord)

			wordList = ['test1', 'test2']
			r = ds.search(wordList)
			for t in r:
				print(t)
		
			ds.closeConnection()
		'''
		self.db_config = read_db_config(configFile)


	def connect(self):
		""" 
			Connects to database
		"""
		try:
			# most connections allowed to Database
			maxconnections = 5

			# create counting semaphore 
			self.pool_sema = threading.BoundedSemaphore(value = maxconnections)

			# create connection pool implicitly
			self.conn = mysql.connector.connect(pool_name="thePool",
												pool_size=maxconnections, # 5 is the default
												**self.db_config)
			if self.conn.is_connected():
				print('connection established.')
			else:
				print('connection failed.')

			# turn off autocommit
			self.conn.autocommit = False


		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Something is wrong with your user name or password")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Database does not exist")
			else:
				print(err)


	# (url, title, Dict<word: (wordCount, excerpt)>)
	def indexPage(self, url, title, words):
		""" Inputs are a url (string), title (string), Dict<word (string), tuple(wordCount (int), excerpt(string)>
		"""

		# with automatically calls acquire and release upon entering and exiting block
		with self.pool_sema:
			# grab connection from pool
			self.conn = mysql.connector.connect(pool_name="thePool")

			try:
				# check lengths: URL <= 255 title <= 100 
				url = str(url[0:255])
				title = str(title[0:100])
				
				# store url & title 
				args = (url, title, 0)

				# start a transaction
				''' SERIALIZABLE is restrictive and does nont all dirty, nonrepeatable or phantom reads
				 might be able to go to less restrictive... '''
				self.conn.start_transaction(isolation_level='SERIALIZABLE')

				# create a cursor to call url procedure
				cursorUrl = self.conn.cursor()

				# results holds the args sent into callproc but contains an output with the uid
				# that is needed in the next mysql procedure call
				results = cursorUrl.callproc('PRC_STORE_URL_TTL', args)
				
				''' NEXT VERSION HAVE MYSQL ITERATE THROUGH LIST OF WORDS '''

				# create a cursor to call store word procedure
				cursorWord = self.conn.cursor()

				# store word, wordcount and excerpt
				for word, wordData in words.items():
					# check lengths: Word <= 45, excerpt <= 150
					word = str(word[0:45])
					excerpt = str(wordData[1][0:150])
					
					# store word id, word, word count and excerpt into db
					args = (word, results[2], wordData[0], excerpt)
					cursorWord.callproc('PRC_STORE_WRD', args)
					
				# call commit
				self.conn.commit()

				# close cursors
				cursorUrl.close()
				cursorWord.close()


			except mysql.connector.Error as err:
				print(err)
			
			# return connection back to pool
			self.conn.close()
			

	# List<word> -> List<(url, title, excerpt, word count)>
	def search(self, words):
		""" Inputs are a list of words
			Returns:
				list of tuples if no problem (maybe empty if words arent in db...), 
				list containing '1' and the error if error storing info, 
				list containing '2' and 'Db not connected' if database is not connected
		"""

		# with automatically calls acquire and release upon entering and exiting block
		with self.pool_sema:
			# grab connection from pool
			self.conn = mysql.connector.connect(pool_name="thePool")

			retList = []

			try:

				
				cursorRetrieve = self.conn.cursor()

				for word in words:
					# find word in database and return a row
					cursorRetrieve.callproc('PRC_FIND_WRD', (word,))

					# add result to return list 
					for result in cursorRetrieve.stored_results():
						#print(result.fetchall())
						retList.append(tuple(result))

				''' DO THIS SECOND
				# pass list of words to database
				args[words]
				self.cursor.callproc('PRC_FIND_WORD', args)

				# add result to return list 
				for result in cursor.stored_results():
					print(result.fetchall())
					#retList.append(result)
				'''
				# close cursor
				cursorRetrieve.close()

			except mysql.connector.Error as err:
				print(err)
		
			# return connection back to pool
			self.conn.close()

			return retList