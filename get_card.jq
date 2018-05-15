jq .KTK.cards|map(select(.name=="Scoured Barrens")) src/chumpblock/data/AllSets-x.json
jq .[].cards|map(select(.name=="Scoured Barrens")) src/chumpblock/data/AllSets-x.json

