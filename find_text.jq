jq '.KTK.cards|map(select(.text|contains("enters the battlefield tapped")))|map({name,text})' src/chumpblock/data/AllSets-x.json

