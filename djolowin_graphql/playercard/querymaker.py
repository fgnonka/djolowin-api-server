playercards_query = {
    "query": """
    { allPlayercards (first: 10) {
        edges{
            node{
                cardId 
                price 
                index
                totalCardIndex
                absoluteUrl
                player{
                    jerseyNumber
                    age
                    name 
                    team{
                        year 
                        country{
                            country
                            }
                        }
                    }
                rarity{
                    name
                }
            }
        }
    } 
}"""
}
