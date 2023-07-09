from datetime import date
from fastapi import FastAPI, HTTPException, Path, Query, status
from book import Book, BookRequest

"""
define the initial books model
"""
BOOKS = [
    Book(1,"Title 1","Kevin","This is 1 book",5,date(2023,1,1)),
    Book(2,"Title 2","Kevin","This is 2 book",2,date(2022,1,1)),
    Book(3,"Title 3","Cathy","This is 3 book",5,date(2021,1,1)),
    Book(4,"Title 4","Kevin","This is 4 book",2,date(2022,1,1)),
    Book(5,"Title 5","Mike","This is 5 book",3,date(2022,1,1)),
    Book(6,"Title 6","Cathy","This is 6 book",1,date(2023,1,1)),
    Book(7,"Title 7","Yuyu","This is 7 book",4,date(2023,1,1)),
    Book(8,"Title 8","Kevin","This is 8 book",2,date(2020,1,1)),
]

app = FastAPI()


@app.get("/books")
async def read_all_books():
    return BOOKS # automatically serialize the data in the response


@app.get("/books/{id}", status_code=status.HTTP_200_OK)
async def get_book_by_id(id:int = Path(gt=0)):
    try:
        #return Response(content=BOOKS[id-1],status_code=200)
        return BOOKS[id-1]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404,detail=f"the book id {id} is not found")
    
@app.get("/books/",status_code=status.HTTP_200_OK)
async def get_books_by_ranting(rating: int=Query(gt=0,lt=6)):
    return list(filter(lambda x:x.rating==rating,BOOKS))

@app.get("/books/publish/{published_date}",status_code=status.HTTP_200_OK,
         summary="get the book which published date is less than input date",
         description="decrpittionn")
async def get_books_by_ranting(published_date: date):

    result = list(filter(lambda x:x.published_date<=published_date,BOOKS))
    if not result:
        raise HTTPException(status_code=404,detail="item not found")
    return result 


@app.post("/book/create",status_code=status.HTTP_201_CREATED)
async def create_book(new_book: BookRequest):
    # Convert he bookrequest to book object with key=value pair parameter and taken in the constructor of Book
    param_dict = new_book.dict()
    param_dict.update({"id":find_book_max_id(BOOKS)})


    book = Book(**param_dict)
    BOOKS.append(book)
    return await read_all_books()


@app.put("/book/update",status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book_request: BookRequest):
    # Convert he bookrequest to book object with key=value pair parameter and taken in the constructor of Book
    for ind,book in enumerate(BOOKS):
        if book.id == book_request.id:
            BOOKS[ind] = Book(**book_request.dict())
            return
    raise HTTPException(status_code=404,detail="Items not found.")


@app.delete("/book/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int = Path(gt=0)):
    # Convert he bookrequest to book object with key=value pair parameter and taken in the constructor of Book
    for ind,book in enumerate(BOOKS):
        if book.id == id:
            BOOKS.pop(ind)
            return 
    raise HTTPException(status_code=404,detail=f"Not found for {id}")
        



# normal function: the function without decorator
def find_book_max_id(books: list) -> int:
    return books[-1].id + 1