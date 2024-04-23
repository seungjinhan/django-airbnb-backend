"""
    raphql 을 위해서 dummy api 생성
"""

import strawberry
from rooms import schema as rooms_schema


@strawberry.type
class Query(
    rooms_schema.Query,
):
    pass


@strawberry.type
class Mutation:
    pass


schema = strawberry.Schema(
    query=Query,
    # mutation=Mutation,
)
# @strawberry.type
# class Movie:
#     pk: int
#     title: str
#     year: int
#     rating: int


# movies_db = [
#     Movie(pk=1, title="GodFather", year=1990, rating=10),
# ]


# def movies() -> typing.List[Movie]:
#     return movies_db


# def movie(movie_id: int) -> Movie:
#     return movies_db[movie_id - 1]


# def add_movie(title: str, year: int, rating: int) -> Movie:
#     m = Movie(pk=len(movies_db) + 1, title=title, year=year, rating=rating)
#     movies_db.append(m)
#     return m


# @strawberry.type
# class Query:
#     movies: typing.List[Movie] = strawberry.field(resolver=movies)
#     movie: Movie = strawberry.field(resolver=movie)


# @strawberry.type
# class Mutation:
#     add_movie: Movie = strawberry.mutation(resolver=add_movie)
