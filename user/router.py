from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from user.schema import UserSignUpRequest, UserResponse, UserLogInRequest
from database.connection import get_session
from user.model import User
from auth.password import hash_password


router = APIRouter(
    prefix="/users",
    tags=["User"]
)

@router.post(
    "",
    summary="회원가입 API",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
async def signup_user_handler(
    body : UserSignUpRequest,
    session = Depends(get_session),
):
    #이메일 중복 검사
    stmt = select(User).where(User.email == body.email)
    result = await session.execute(stmt)
    user = result.scalar()
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 가입된 이메일 주소입니다."
        )

    #비밀번호 해싱
    hashed_password = hash_password(plain_password=body.password)

    new_user = User(
        email=body.email, hashed_password=hashed_password
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user


@router.post(
    "/login",
    summary="로그인 API",
    status_code=status.HTTP_200_OK,
)
async def login_user_handler(
    body: UserLogInRequest,

):
