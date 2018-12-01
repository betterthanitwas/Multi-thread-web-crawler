import mysql.connector
from mysql.connector import errorcode
from python_mysql_dbconfig import read_db_config
import threading

class DataStore:
	def __init__(self, config_file):
		'''
		Example:
			ds = DataStore('config.ini')

			url = 'www.Thisisatest.com'
			title = 'Test Title'
			dict_word = {'test1': (50, "this test1 word is a test excerpt"),
						'test2': (10, "this test2 : excerpt")}
			ds.indexPage(url, title, dict_word)

			word_list = ['test1', 'test2']
			r = ds.search(word_list)
			for t in r:
				print(t)
		'''
		# holds configuration data (user, password, etc) for db connection
		self.db_config = read_db_config(config_file)

		# most connections allowed to Database and semaphore
		self.max_connections = 5
		# create counting semaphore 
		self.pool_sema = threading.BoundedSemaphore(value = self.max_connections)


	# (url, title, Dict<word: (wordCount, excerpt)>)
	def indexPage(self, url, title, words):
		""" Inputs are a url (string), title (string), Dict<word (string), tuple(wordCount (int), excerpt(string)>
		"""

		# check lengths: URL <= 255 title <= 100 
		url = str(url[0:255])
		title = str(title[0:100])
		arg_url = (url, title, 0)


		# with automatically calls acquire and release upon entering and exiting block
		with self.pool_sema:

			# use connection pool implicitly
			conn = mysql.connector.connect(pool_name="thePool",
												pool_size=self.max_connections, # 5 is the default
												**self.db_config)

			try:
				
				# turn off autocommit
				conn.autocommit = False

				# start a transaction
				''' SERIALIZABLE is restrictive and does not allow dirty, nonrepeatable or phantom reads
				 might be able to go to less restrictive... '''
				conn.start_transaction(isolation_level='SERIALIZABLE')

				# create a cursor to call procedure
				cursor = conn.cursor()
					
				# call procedure to add url, title
				results = cursor.callproc('PRC_STORE_URL_TTL', arg_url)


				# word, wordcount and excerpt to arg list
				for word, word_data in words.items():
					# check lengths: Word <= 45, excerpt <= 150
					word = str(word[0:45])
					excerpt = str(word_data[1][0:150])
					
					# add word, url id, word count and excerpt to args
					arg_list = (word, results[2], word_data[0], excerpt)
					# add word info to Db
					cursor.callproc('PRC_STORE_WORD', arg_list)
					
					
				# call commit
				conn.commit()
				
				# close cursors
				cursor.close()


			except mysql.connector.Error as err:
				print(err)
			
			# return connection back to pool
			conn.close()
			

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

			# use connection pool implicitly
			conn = mysql.connector.connect(pool_name="thePool",
												pool_size=self.max_connections, # 5 is the default
												**self.db_config)

			return_list = []

			try:
				# create a cursor to call search procedure
				cursor_retrieve = conn.cursor()

				for word in words:
					# find word in database and return a row
					cursor_retrieve.callproc('PRC_FIND_WRD', (word,))

					# add result to return list 
					for result in cursor_retrieve.stored_results():
						#print(result.fetchall())
						return_list.append(tuple(result))

				# close cursor
				cursor_retrieve.close()

			except mysql.connector.Error as err:
				print(err)
		
			# return connection back to pool
			conn.close()

			return return_list
