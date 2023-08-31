from py2neo import Graph
from tqdm import tqdm

graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

def generate_recommendations():
    results = graph.run(
    '''
    MATCH (user: User)
    CALL {
        WITH user
        MATCH (user) -[user2Ratings:Rating]-> (likedUser2Animes: Anime) -[similarities:Similar]-> (similarAnimes:Anime)
        RETURN similarAnimes.anime_id AS recomended_anime_id, similarAnimes.name AS recomended_anime_name, SUM(similarities.gosteis) AS gosteis
        ORDER BY gosteis DESC
        LIMIT 3
    }
    RETURN user.user_id AS target_user, recomended_anime_id, recomended_anime_name, gosteis
    '''
    )

    results_list = results.data()

    recomendations = {}

    for rec in results_list:
        if rec['target_user'] not in recomendations:
            recomendations[rec['target_user']] = []
            
        recomendations[rec['target_user']].append({
            'id': rec['recomended_anime_id'],
            'name': rec['recomended_anime_name']
        })
    
    return recomendations

