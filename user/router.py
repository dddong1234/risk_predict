from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from user.schema import UserSignUpRequest, UserResponse, UserLogInRequest
from database.connection import get_session
from user.model import User
from auth.password import hash_password, verify_password
from auth.jwt import create_access_token, verify_access_token, verify_user


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
    session = Depends(get_session),

):
    stmt = select(User).where(User.email == body.email)
    result = await session.execute(stmt)
    user = result.scalar()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일과 비밀번호가 일치하지 않습니다."
        )
    is_verified = verify_password(
        password = body.password,
        hashed_password=user.hashed_password
    )
    if not is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일과 비밀번호가 일치하지 않습니다."
        )

    access_token = create_access_token(user_id=user.id)

    return {"access_token": access_token}

@router.get(
    "/me",
    summary="내 정보 조회 API",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
async def get_me_handler(
    session = Depends(get_session),
    user_id = Depends(verify_user),
):
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar()

    return user

