from fastapi import APIRouter , HTTPException , Depends , status , Response
from app.dependencies import get_current_user
from sqlalchemy.orm import Session
from app.database import get_db
from sqlalchemy import select
from app.models import User , Note
from app.schemas import GetUserResponse , GetNoteListResponse , CreateNoteRequest , GetNoteResponse , PatchNoteRequest

router = APIRouter(
    prefix="/api",
    tags=["bussiness"]
)


@router.get(
    "/users/me",
    response_model=GetUserResponse
)
def get_user(
    user : User = Depends(get_current_user)
) :
    ret = {
        "id" : user.id,
        "username" : user.username,
        "created_at" : user.created_at,
        "is_active" : user.is_active,
        "notes_num" : len(user.notes),
    }
    
    return ret


@router.get(
    "/notes",
    response_model=list[GetNoteListResponse]
)
def get_note_list(
    user : User = Depends(get_current_user)
) :
    notes = list(user.notes)

    # 处理置顶
    notes.sort(key=lambda x : x.is_pinned , reverse=True)

    return notes


@router.post(
    "/notes",
    status_code=status.HTTP_204_NO_CONTENT
)
def create_note(
    data : CreateNoteRequest,
    user : User = Depends(get_current_user),
    db : Session = Depends(get_db)
) :
    note = Note(
        title = data.title,
        content = data.content,
        author_id = user.id,
    )

    db.add(note)
    db.commit()
    db.refresh(note)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/notes/{note_id}",
    response_model=GetNoteResponse
)
def get_note(
    note_id : int,
    user : User = Depends(get_current_user),
    db : Session = Depends(get_db)
) :
    note = db.execute(
        select(Note).where(Note.id == note_id)
    ).scalar_one_or_none()

    if note is None :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="note not found"
        )

    if note.author_id != user.id :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorized"
        )

    return note



@router.patch(
    "/notes/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def patch_note(
    note_id : int ,
    data : PatchNoteRequest,
    user : User = Depends(get_current_user),
    db : Session = Depends(get_db)
) :
    note = db.execute(
        select(Note).where(Note.id == note_id)
    ).scalar_one_or_none()

    if note is None :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="note not found"
        )

    if note.author_id != user.id :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorized"
        )

    if data.title is not None :
        note.title = data.title

    if data.content is not None :
        note.content = data.content

    db.commit()
    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )


@router.delete(
    "/notes/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_note(
    note_id : int,
    user : User = Depends(get_current_user),
    db : Session = Depends(get_db)
) :
    note = db.execute(
        select(Note).where(Note.id == note_id)
    ).scalar_one_or_none()

    if note is None :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="note not found"
        )

    if note.author_id != user.id :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authoized"
        )

    db.delete(note)
    db.commit()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )


@router.post(
    "/notes/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def change_pinned_status(
    note_id : int,
    user : User = Depends(get_current_user),
    db : Session = Depends(get_db)
) :
    note = db.execute(
        select(Note).where(Note.id == note_id)
    ).scalar_one_or_none()

    if note is None :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="note not found"
        )

    if note.author_id != user.id :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authoized"
        )

    note.is_pinned = not note.is_pinned

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )