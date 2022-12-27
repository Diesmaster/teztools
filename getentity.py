import requests
import json
import pandas as pd
import sys

query_test="""query MyQuery {
  token(
    where: {name: {_eq: "Looking out at the sea"}, creators: {_and: {creator_address: {_eq: "tz1g7uHLzMJt3c1BFzyGmftvYvPw5AiJEkGL"}}}}
  ) {
    artifact_uri
    average
    decimals
    description
    display_uri
    extra
    flag
    highest_offer
    is_boolean_amount
    last_listed
    last_metadata_update
    level
    lowest_ask
    metadata
    mime
    name
    ophash
    rights
    supply
    symbol
    thumbnail_uri
    timestamp
    tzip16_key
  }
}"""


query_get_artists = """query MyQuery {
  holder(where: {address: {_eq: "tz1Xkn7QYfbqsHpD7bUAkYeE9LZu3kK3T7vj"}}) {
    twitter
    owner_operators {
      token {
        creators {
          creator_address
        }
      }
    }
  }
}"""

objkt_explorer="https://data.objkt.com/v3/graphql"

print("hello world")


def reqObjkt(query):
	r = requests.post(objkt_explorer, json={'query': query})
	#print(r.status_code)
	#print(r.text)
	return r

r = reqObjkt(query_get_artists)
json_data = json.loads(r.text)

#print(json_data['data']['holder'][0]['owner_operators'])

unique_addies = []

for token in json_data['data']['holder'][0]['owner_operators']:
	#print(token)
	for creators in token['token']['creators']:
		if creators['creator_address'] not in unique_addies:
           		unique_addies.append(creators['creator_address'])


unique_tokens = []

for addy in unique_addies:
	buyable_token = """query MyQuery {
  token(
    where: {creators: {creator_address: {_eq: \"""" + addy + """\" }, _and: {}}, _and: {listings: {amount_left: {_eq: 1}}}}
  ) {
    fa {
      contract
    }
    name
  }
}"""

	buyable_token = """query MyQuery {
  token(
    where: {creators: {creator_address: {_eq: \"""" + addy + """\"}}, _and: {listings: {status: {_eq: "active"}, amount_left: {_eq: """ + sys.argv[1] + """}, seller_address: {_eq: \"""" + addy + """\"}}}, , supply: {_gt: "1"}}
  ) {
    fa {
      contract
    }
    name
    token_id
    listings(where: {status: {_eq: "active"}}) {
      price_xtz
    }
    listing_sales(order_by: {price_xtz: asc}) {
      price_xtz
    }
  }
}"""
	r = reqObjkt(buyable_token)
	json_data = json.loads(r.text)
	#print(json_data)
	#print(buyable_token)
	if len(json_data['data']['token']) > 0:
		if len(json_data['data']['token'][0]['listing_sales']) > 0:
			if json_data['data']['token'][0]['listings'][0]['price_xtz'] <= json_data['data']['token'][0]['listing_sales'][0]['price_xtz']:
				print(json_data['data']['token'][0]['fa']['contract'] + "/" + json_data['data']['token'][0]['token_id'] )


#print(unique_addies)
#df_data = json_data
#df = pd.DataFrame(df_data)
