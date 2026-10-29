from fastapi import APIRouter

from app.api.v1 import admin, auth, chat, community, community_feed, health, oauth, problems, submissions, topics, users

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(oauth.router)
api_router.include_router(users.router)
api_router.include_router(admin.router)
api_router.include_router(problems.router)
api_router.include_router(topics.router)
api_router.include_router(submissions.router)
api_router.include_router(community.router)
api_router.include_router(community_feed.router)
api_router.include_router(chat.router)
