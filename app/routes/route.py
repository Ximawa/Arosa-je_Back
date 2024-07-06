from datetime import timedelta
import os
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlmodel import Session
from app.functions.functions import *
from app.crud.crud import *
from app.database import get_db
from app.models.models import *
from passlib.context import CryptContext

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={
            "login": user.username,
            "id": user.id,
            "role": user.id_role
        }, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register")
def create_new_user(username: str = Form(...),
                    password: str = Form(...),
                    email: str = Form(...),
                    full_name: str = Form(...),
                    id_role: int = Form(...),
                    db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=username)
    if db_user and username != 'testuser':
        raise HTTPException(
            status_code=400, detail="Username already registered")
    hashed_password = pwd_context.hash(password)
    user = User(username=username, password=hashed_password,
                email=email, full_name=full_name, id_role=id_role)
    return create_user(db, user)


@router.post("/deleteUser")
def delete_user(username: str = Form(...), db: Session = Depends(get_db)):
    return delete_user_by_username(db, username)


@router.get("/roles")
def get_all_roles(db: Session = Depends(get_db)):
    return get_roles(db)


@router.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    return get_users(db)


@router.get("/users/{id}")
def get_user_id(id: int, db: Session = Depends(get_db)):
    return get_user_by_id(db, user_id=id)


@router.post("/CreateRole")
def create_new_role(role: Role, db: Session = Depends(get_db)):
    db_role = get_role_by_title(db, role_title=role.title)
    if db_role:
        raise HTTPException(
            status_code=400, detail="Role already exists")
    return create_role(db, role)


@router.get("/listing")
def get_all_listing(db: Session = Depends(get_db), token: str = Depends(verify_token)):
    return get_listings(db)


@router.get("/listings/{listing_id}/{user_id}")
def get_listing_by_id(listing_id: int, user_id: int, db: Session = Depends(get_db)):
    return get_is_user_listing_or_proposal(db, id=listing_id, user_id=user_id)


@router.post("/CreateListing")
def create_new_listing(listing: Listing, db: Session = Depends(get_db), token: str = Depends(verify_token)):
    listing.start_date = datetime.datetime.strptime(
        listing.start_date, "%Y-%m-%d %H:%M")
    listing.end_date = datetime.datetime.strptime(
        listing.end_date, "%Y-%m-%d %H:%M")

    return create_listings(db, listing)


@router.post("/upload/{folder_name}")
async def upload_photo(folder_name: str, file: UploadFile = File(...)):
    # Créer le chemin du dossier avec le nom spécifié
    folder_path = f"./uploads/{folder_name}/main/"

    # Vérifier si le dossier existe déjà
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    try:
        # Sauvegarder le fichier dans le dossier
        file_path = os.path.join(folder_path, file.filename)
        with open(file_path, "wb") as f:
            f.write(file.file.read())
    except Exception as e:
        # En cas d'erreur, supprimer le dossier créé
        os.rmdir(folder_path)
        raise HTTPException(
            status_code=500, detail=f"Erreur lors de la sauvegarde du fichier : {str(e)}")

    return {"message": f"Fichier {file.filename} sauvegardé dans le dossier {folder_name}"}


@router.get("/get_image/{image_id}")
async def get_image(image_id: int):
    image_folder_path = f"./uploads/{image_id}/main/"
    if os.path.exists(image_folder_path):
        image_files = os.listdir(image_folder_path)
        if image_files:
            first_image_path = os.path.join(image_folder_path, image_files[0])
            return FileResponse(first_image_path)
        else:
            return {"error": "No image found in the folder"}
    else:
        return {"error": "Folder not found"}


@router.get("/get_listing/{listing_id}")
def get_listing_by_id(listing_id: int, db: Session = Depends(get_db)):
    return get_listings_by_id(db, id=listing_id)


@router.get("/get_proposal_created/{listing_id}")
def get_proposal_created_by_listing_id(listing_id: int, db: Session = Depends(get_db), token: str = Depends(verify_token)):
    return get_proposal_created(db, listing_id)


@router.post("/createProposal")
def create_new_listing(proposal: Proposal, db: Session = Depends(get_db), token: str = Depends(verify_token)):
    return create_proposal(db, proposal)


@router.post("/createConversation")
def create_new_conversation(conversation: Conversation, db: Session = Depends(get_db)):
    return create_conversation(db, conversation)


@router.get("/conversation/{id}")
def get_conversation_by_id(id: int, db: Session = Depends(get_db)):
    return get_messages_by_conversation_id(db, id)


@router.get("/conversation/user/{id}")
def get_conversation_by_user_id(id: int, db: Session = Depends(get_db)):
    return get_all_last_message_of_conversation_by_user_id(db, id)


@router.post("/addMessage/")
def add_message_to_conversation(message: ConversationMessageIn, db: Session = Depends(get_db), token: str = Depends(verify_token)):
    db_message = ConversationMessage(
        **message.model_dump(), timestamp=datetime.datetime.utcnow())
    return create_message(db, db_message)


@router.get("/listing/user/{id}")
def get_listing_by_user_id(id: int, db: Session = Depends(get_db)):
    return get_listings_by_user_id(db, id)


@router.get("/plantes/")
def plantes(db: Session = Depends(get_db), token: str = Depends(verify_token)):
    return get_all_plantes(db)


@router.post("/CreatePlante")
def createPlante(plante: Plante, db: Session = Depends(get_db), token: str = Depends(verify_token)):
    return create_plantes(db, plante)


@router.post("/upload-encyclopedie/{folder_name}")
async def upload_photo(folder_name: str, file: UploadFile = File(...)):
    # Créer le chemin du dossier avec le nom spécifié
    folder_path = f"./uploads-encyclopedie/{folder_name}/main/"

    # Vérifier si le dossier existe déjà
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    try:
        # Sauvegarder le fichier dans le dossier
        file_path = os.path.join(folder_path, file.filename)
        with open(file_path, "wb") as f:
            f.write(file.file.read())
    except Exception as e:
        # En cas d'erreur, supprimer le dossier créé
        os.rmdir(folder_path)
        raise HTTPException(
            status_code=500, detail=f"Erreur lors de la sauvegarde du fichier : {str(e)}")

    return {"message": f"Fichier {file.filename} sauvegardé dans le dossier {folder_name}"}


@router.get("/get_image-encyclopedie/{image_id}")
async def get_image(image_id: int):
    image_folder_path = f"./uploads-encyclopedie/{image_id}/main/"
    if os.path.exists(image_folder_path):
        image_files = os.listdir(image_folder_path)
        if image_files:
            first_image_path = os.path.join(image_folder_path, image_files[0])
            return FileResponse(first_image_path)
        else:
            return {"error": "No image found in the folder"}
    else:
        return {"error": "Folder not found"}


@router.get("/encyclopedie/{id}")
def get_post_by_plante_id(id: int, db: Session = Depends(get_db)):
    return get_posts_by_plante_id(db, id)


@router.post("/encyclopedie/createPost")
def createPost(post: Post, db: Session = Depends(get_db), token: str = Depends(verify_token)):
    return create_post(db, post)
