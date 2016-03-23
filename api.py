"""Connects to the orcid API, searches using a given query and puts results into database"""

import orcid

# oew1v07's Public API key and secret. Will need to be changed if oew1v07 leaves
# group at any time according to orcid T&Cs
KEY = "APP-RQFHFHDT5CO7FZDN"
SECRET = "bde7e6b4-f633-4e4b-b749-4efc855fb797"

class API(object):

	def __init__(self):
		self.connect()
	
	def connect(self):
		"""Connects to the orcid api to provide handle for searching"""
		self.P_api = orcid.PublicAPI(KEY, SECRET)

	def search(self, query):
		"""Searches for a specific phrase within orcid-bio returning a generator

		Args
		----
		query: String
			The university to be searched for. For example "Manchester"

		Attributes
		----------
		self.result_generator: generator
			Generator for all results provided from the search query.
			To get the next result the function next(self.result_generator)
			should be used
		self.num_returned
			The number of results from the search
		"""

		P_res = self.P_api.search_public(query)

		self.num_returned = P_res['orcid-search-results']['num-found']

		self.result_generator = self.P_api.search_public_generator(query)

	def store_results(self):
		"""Puts results from search into a neo4j database"""
		pass
