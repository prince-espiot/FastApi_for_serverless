#building and releasing iOS/Android apps

from typing import List, Optional
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException

from models import User, Gender, Role, UserUpdate

app = FastAPI()

db: List[User]=[
    User(id=uuid4(), first_name="Prince", last_name="Okumo", middle_name="dzan", gender=Gender.male, role=[Role.admin, Role.user]),
    User(id=uuid4(), first_name="Liz", last_name="adzangbo",  gender=Gender.female, role=[Role.student]),
    User(id=uuid4(), first_name="stewie", last_name="family", middle_name="guy", gender=Gender.male, role=[Role.user])

]

@app.get("/")
def root () ->dict: 
    return {"Hello": "Prince"}

@app.get("/api/v1/users")
async def fetch_users():
    return db

@app.get("/users/first_name")
def get_user_first_names() -> List[str]:
    return [user.first_name for user in db]

@app.get("/users/find")  #GET http://127.0.0.1:8000/users/find?first_name=Prince #GET http://127.0.0.1:8000/users/find?last_name=Adzangbo
#GET http://127.0.0.1:8000/users/find?first_name=Liz&last_name=Adzangbo
def find_user_by_name(first_name: Optional[str] = None, last_name: Optional[str] = None) -> List[User]:
    """
    Find users by first name or last name.
    - `first_name`: Filter by first name
    - `last_name`: Filter by last name
    """
    if not first_name and not last_name:
        raise HTTPException(status_code=400, detail="Provide at least 'first_name' or 'last_name' as a query parameter.")

    result = [
        user for user in db
        if (first_name and user.first_name.lower() == first_name.lower()) or
           (last_name and user.last_name.lower() == last_name.lower())
    ]

    if not result:
        raise HTTPException(status_code=404, detail="No users found with the given name.")

    return result

@app.get("/users/role/user")  #http://127.0.0.1:8000/users/role/user
def get_users_with_role_user() -> List[User]:
    """
    Get users with the role 'user'.
    """
    result = [user for user in db if Role.user in user.role]
    return result


@app.delete("/users/{user_id}")
def delete_user(user_id: UUID) -> dict:
    """
    Delete a user by their UUID.
    """
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return {"message": f"User with ID {user_id} has been deleted."}
    
    # If the user is not found, raise an HTTPException
    raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found.")

@app.put("/users/{user_id}")
def update_user(user_id: UUID, user_update: UserUpdate) -> dict:
    """
    Update user details by UUID.
    """
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            """ if user_update.gender is not None:
                user.gender = user_update.gender """
            if user_update.role is not None:
                user.role = user_update.role
            
            return {"message": f"User with ID {user_id} has been updated.", "user": user}
    
    # If the user is not found, raise an HTTPException
    raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found.")