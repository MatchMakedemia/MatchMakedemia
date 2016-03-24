
# Gets the non None relationship graph
"START n=node(*) match n-[r:HAS]-(s) WHERE NOT s.value = "None" return r limit 25"

#All tags which have more than one HAS relationship

match (k:Keyword)-[r:HAS]-() WITH k, r, count(r) as links WHERE links > 0 AND NOT k.value = "None" return k, count(r), r

match (k:Keyword)-[r:HAS]-() WITH k, r, count(r) as links WHERE links > 0 AND NOT k.value = "None" return k, links, r ORDER BY links