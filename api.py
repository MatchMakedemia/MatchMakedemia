"""Connects to the orcid API, searches using a given query and puts results into database"""
# Remember to be in the right email

import orcid
from py2neo import Graph, Node, Relationship, authenticate
import sys

# oew1v07's Public API key and secret. Will need to be changed if oew1v07 leaves
# group at any time according to orcid T&Cs
KEY = "APP-RQFHFHDT5CO7FZDN"
SECRET = "bde7e6b4-f633-4e4b-b749-4efc855fb797"
BASEPATH = "http://orchid.org/"
db_user = "neo4j"
db_passwd = "match2016"


class API(object):

	def __init__(self):
		self.connect_api()
		self.connect_db()
	
	def connect_api(self):
		"""Connects to the orcid api to provide handle for searching"""
		self.P_api = orcid.PublicAPI(KEY, SECRET)

	def connect_db(self):
		authenticate("localhost:7474", db_user, db_passwd)
		self.graph = Graph("http://localhost:7474/db/data")

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

		# Make sure which query was used is in the object
		self.query = query

		P_res = self.P_api.search_public(query)

		self.num_returned = P_res['orcid-search-results']['num-found']

		self.result_generator = self.P_api.search_public_generator(query)

	def store_results(self):
		"""Puts results from search into a neo4j database"""
		# To get the bio from each result
		for i in range(self.num_returned):
			next_res = next(self.result_generator)

			bio = next_res["orcid-profile"]["orcid-bio"]

			if bio is None:
				pass
			else:
				# This is a dict inside a list inside a dict inside a dict.
				# It returns a string of each of the keywords
				if bio["keywords"] is None:
					keywords = None
				else:
					keywords = bio["keywords"]["keyword"][0]["value"]

				given_name = bio["personal-details"]["given-names"]["value"]
				family_name = bio["personal-details"]["family-name"]["value"]
				name = given_name + " " + family_name

				# orcid path is the orcid ID which can be joined with BASEPATH to get
				# URL of profile
				orcid_path = next_res["orcid-profile"]["orcid-identifier"]["path"]

				# Always remember to create after each node!!!!!
				# Create the person node
				person = Node("Person", name = name, orcid = orcid_path)
				self.graph.create(person)
				# We have to check whether the keyword node already exists and if so 
				# then link to that.

				# Get handle for the None keyword
				none = self.graph.find_one("Keyword", property_key="value", 
										   property_value="None")

				if keywords is None:
					# create a relationship with the keyword none
					rel = Relationship(person, "HAS", none)
					self.graph.create(rel)
				else:
					list_keywords = keywords.split(",")

					key_nodes = []
					for i in list_keywords:
						# Create keyword node
						handle = new_api.graph.find_one("Keyword", property_key="value", property_value="i")
						if handle:
							rel = Relationship(person, "HAS", handle)
						else:
							new = Node("Keyword", value = i)
							self.graph.create(new)
							rel = Relationship(person, "HAS", new)

						# Create relationship with person
						self.graph.create(rel)

				# Create institution node
				institution_name = "University of " + self.query

				inst_handle = new_api.graph.find_one("Institution",
													 property_key="value",
													 property_value=institution_name)

				if inst_handle:
					rel2 = Relationship(person, "ISMEMBEROF", inst_handle)
				else:
					institution = Node("Institution", value = institution_name)
					self.graph.create(institution)
					rel2 = Relationship(person, "ISMEMBEROF", inst_handle)
				# Create a relationship of ISMEMBEROF with person and institution
				
				self.graph.create(rel2)

def run_class(query):
	api = API()
	api.search(query)
	api.store_results()
	return api


# graph.cypher.execute("MATCH (p:person) RETURN p.name AS name")

