from fastapi import FastAPI
from pydantic import BaseModel

Movies = {}


class Movie(BaseModel):
    Name: str
    Genre: str
    Year: int
    Length: str


app = FastAPI()


@app.get("/get_movies")
def get_movie():
    return Movies


@app.put("/add_movie")
def add_movie(movie: Movie):
    if not movie.dict() in Movies.values():
        Movie_ID = Movies.__len__() + 1
        newMovie = {Movie_ID: movie.dict()}
        Movies.update(newMovie)
        return Movies
    else:
        return f"Movie with Name: {movie.Name} already exists."


@app.get("/SearchBy/{Year or Genre}")
def search_movie(Year: int = None, Genre: str = None):
    MovieToShow = {}

    if Movies.__len__() == 0:
        return "404 Not Found!"
    else:
        for key, value in Movies.items():

            if Genre is None and Year == value["Year"]:
                print("Only id", Genre, Year)
                MovieToShow.update({key: value})
            elif Year is None and Genre == value["Genre"]:
                print("Only Genre", Genre, Year)
                MovieToShow.update({key: value})
            elif Year == value["Year"] and Genre == value["Genre"]:
                print("Both", Genre, Year)
                MovieToShow.update({key: value})

            elif (Year == value["Year"] and Genre != value["Genre"]) or (
                    Year != value["Year"] and Genre == value["Genre"]):
                print("mixed", Genre, Year)
                print(value["Year"], value["Genre"])

        if not MovieToShow:
            return "Movie Not Found!"

        return MovieToShow


@app.put("/UpdateBy/{Movie_ID}")
def update_by_id(Movie_ID: int, Name: str = None, Genre: str = None, Year: int = None, Length: str = None):
    if Movie_ID in Movies.keys():
        if Name is not None:
            Movies[Movie_ID]["Name"] = Name
        if Genre is not None:
            Movies[Movie_ID]["Genre"] = Genre
        if Year is not None:
            Movies[Movie_ID]["Year"] = Year
        if Length is not None:
            Movies[Movie_ID]["Length"] = Length
        return f"Movie updated to Name: {Name} | Genre: {Genre} | Year: {Year} | Length: {Length}"
    else:
        return f"ID: {Movie_ID} is out of range!"


@app.delete("/DeleteBy/{Movie_ID}")
def delete_by_id(Movie_ID: int):
    if Movie_ID in Movies.keys():
        mname = Movies[Movie_ID]["Name"]
        del Movies[Movie_ID]
        return f"Movie with Name: < {mname} > is deleted."
    else:
        return f"ID: {Movie_ID} is out of range!"
