from fastapi import FastAPI, HTTPException, Body
from book_dto import BOOKS

apps = FastAPI()

@apps.get("/books")
async def read_all_books() -> list:
    return BOOKS
    #return {"message":"hello world"}


# the function is matter when there are multiple function can handle the same request.
@apps.get("/books/Title 1")
async def get_book():
    return BOOKS[-1]


# book_title: path parameter, #category: query parameter
@apps.get("/books/{book_title}")
async def get_book_by_name(book_title: str,category: str):
    for book in BOOKS:
        if book_title.upper() == book.get("Title").upper():
            return list(
                filter(
                    lambda x:x.get("Category")==category and x.get("Title")==book_title,
                    BOOKS
                ))
    raise  HTTPException(status_code=404, detail=f"the book name '{book_title}' is not found")


@apps.post("/books/create")
# give body's default value
async def create_book(new_book:dict=Body({"Title":"Title 1","Category":"category"})):
    BOOKS.append(new_book)
    return await read_all_books()

@apps.put("/books/update")
async def update_book(updated_book:dict=Body({"Title":"Title 1","Category":"category"})):
    is_found = False
    for ind,book in enumerate(BOOKS):
        if book.get("Title").upper() == updated_book.get("Title").upper():
            BOOKS[ind] = updated_book
            is_found = True
    if is_found:
        return "Success update"
    raise HTTPException(404,f"The book '{updated_book.get('Title')}' is not found")


@apps.delete("/books/{book_title}")
async def delete_book(book_title:str):
    global BOOKS
    filtered_book = list()
    for ind,book in enumerate(BOOKS):
        if book.get("Title").upper() != book_title.upper():
            filtered_book.append(book)
    BOOKS = filtered_book
    return "Success to delete"




       
