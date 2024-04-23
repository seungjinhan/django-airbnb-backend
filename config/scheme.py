"""
    raphql 을 위해서 dummy api 생성
"""

import strawberry
import typing


@strawberry.type
class Movie:
    pk: int
    title: str
    year: int
    rating: int


movies_db = [
    Movie(pk=1, title="GodFather", year=1990, rating=10),
]


@strawberry.type
class Query:
    @strawberry.field
    def movies(self) -> typing.List[Movie]:
        return movies_db

    @strawberry.field
    def movie(self, movie_id: int) -> Movie:
        return movies_db[movie_id - 1]


@strawberry.type
class Mutation:

    @strawberry.mutation
    def add_movie(self, title: str, year: int, rating: int) -> Movie:
        m = Movie(pk=len(movies_db) + 1, title=title, year=year, rating=rating)
        movies_db.append(m)
        return m


schema = strawberry.Schema(query=Query, mutation=Mutation)
