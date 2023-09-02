from py2neo import Graph

graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

def generate_recommendations():
    results = graph.run(
    '''
    MATCH (user: User)
    CALL {
        WITH user
        MATCH (user) -[user2Ratings:Rating]-> (likedUser2Animes: Anime) -[similarities:Similar]-> (similarAnimes:Anime)
        RETURN similarAnimes.anime_id AS recomended_anime_id, similarAnimes.name AS recomended_anime_name, similarAnimes.img AS recomended_anime_img, SUM(similarities.gosteis) AS gosteis
        ORDER BY gosteis DESC
        LIMIT 3
    }
    RETURN user.user_id AS target_user, recomended_anime_id, recomended_anime_name, recomended_anime_img
    '''
    )

    results_list = results.data()

    recomendations = {}  # {<user_id>: [<rec1>, <rec2>, <rec3>]}

    # Cada rec será um registro contendo:
    # target_user: id do usuário que recebeu as recomendações
    # recomended_anime_id, recomended_anime_name e recomended_anime_img: dados sobre o anime recomendado
    for rec in results_list:
        if rec['target_user'] not in recomendations:  
            # Se o usuário ainda não recebeu nenhuma recomendação (primeira vez que aparece como "target_user")
            # então inicializar sua lista de recomendações (inicialmente vazia)
            recomendations[rec['target_user']] = []
            
        recomendations[rec['target_user']].append({
            'id': rec['recomended_anime_id'],
            'name': rec['recomended_anime_name'],
            'img': rec['recomended_anime_img']
        })
    
    return recomendations

