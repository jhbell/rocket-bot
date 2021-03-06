import os
import aiohttp

from aiohttp import web

from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp

router = routing.Router()
routes = web.RouteTableDef()

@router.register("pull_request", action="opened")
async def pull_request_opened_event(event, gh, *args, **kwargs):
    """ Whenever an issue is opened, greet the author and say thanks."""
    issue_url = event.data["pull_request"]["issue_url"]
    url = f"{issue_url}/reactions"
    accept = "application/vnd.github.squirrel-girl-preview+json"
    print(issue_url)
    print(url)
    print(accept)

    await gh.post(url, data={"content": "rocket"}, accept=accept)


@routes.post("/")
async def main(request):
    body = await request.read()

    secret = os.environ.get("GH_SECRET")
    oauth_token = os.environ.get("GH_AUTH")

    event = sansio.Event.from_http(request.headers, body, secret=secret)

    async with aiohttp.ClientSession() as session:
        gh = gh_aiohttp.GitHubAPI(session, "jhbell", oauth_token=oauth_token)
        await router.dispatch(event, gh)
    return web.Response(status=200)

if __name__ == "__main__":
    app = web.Application()
    app.add_routes(routes)
    port = os.environ.get("PORT")
    if port is not None:
        port = int(port)

    web.run_app(app, port=port)
