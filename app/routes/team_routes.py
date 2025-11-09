from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from app.libs.jwt import verify_token
from app.models.team_model import TeamCreateDto, TeamJoinDto, TeamExitDto
from app.services.team_service import createTeam, joinTeam, exitTeam, getTeamInfo, getTeams, disqualifyUserFromTeam

router = APIRouter()

@router.get("/list")
async def get_teams():
    return getTeams()

@router.post("/create")
async def creaet_team(request: Request, userUid: str = Depends(verify_token)):
    """
    디버그 라우트: 들어오는 원본 바디/헤더를 출력하고
    Pydantic 검증 에러가 있으면 상세히 반환합니다.
    """
    try:
        body = await request.json()
    except Exception:
        raw = await request.body()
        body = raw.decode("utf-8", errors="replace")

    # 서버 로그(터미널)에 출력
    print("[DEBUG] /api/team/create headers:", dict(request.headers))
    print("[DEBUG] /api/team/create body:", body)

    # Pydantic 모델로 수동 검증 시도 (pydantic v2)
    try:
        dto = TeamCreateDto.model_validate(body) if isinstance(body, dict) else TeamCreateDto.model_validate_json(body)
    except ValidationError as e:
        print("[DEBUG] ValidationError:", e.errors())
        return JSONResponse(status_code=422, content={"detail": e.errors(), "received": body})

    # 정상인 경우 기존 로직 호출
    return createTeam(userUid, dto)

@router.post("/join")
async def join_team(teamJoinDto: TeamJoinDto, userUid: str = Depends(verify_token)):
    return joinTeam(teamJoinDto, userUid)

@router.post("/exit")
async def exit_team(teamExitDto: TeamExitDto, userUid: str = Depends(verify_token)):
    return exitTeam(teamExitDto, userUid)

@router.get("/info/{teamUid}")
async def get_team_info(teamUid: str):
    return getTeamInfo(teamUid)

@router.get("/disqualify")
async def disqualify_teams(userUid: str = Depends(verify_token)):
    return disqualifyUserFromTeam(userUid)