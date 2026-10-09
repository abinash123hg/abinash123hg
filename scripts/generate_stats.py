#!/usr/bin/env python3
"""Generate profile stats SVGs from the public GitHub REST API."""
import json, os, urllib.request, html
USER="abinash123hg"
headers={"Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2022-11-28"}
if os.getenv("GITHUB_TOKEN"): headers["Authorization"]="Bearer "+os.environ["GITHUB_TOKEN"]
def get(path):
 req=urllib.request.Request("https://api.github.com"+path,headers=headers)
 with urllib.request.urlopen(req,timeout=15) as response: return json.load(response)
try:
 user=get("/users/"+USER); repos=get("/users/"+USER+"/repos?per_page=100&sort=updated")
 stars=sum(r.get("stargazers_count",0) for r in repos); langs={}
 for r in repos:
  if r.get("language"): langs[r["language"]]=langs.get(r["language"],0)+1
 lines="".join(f'<text x="40" y="{155+i*28}" font-size="20">{html.escape(k)}: {v} repositories</text>' for i,(k,v) in enumerate(sorted(langs.items(),key=lambda x:x[1],reverse=True)[:5]))
 body=f'<text x="40" y="55" font-size="28">GitHub activity · {USER}</text><text x="40" y="105" font-size="22">Public repositories: {user.get("public_repos",0)} · Stars: {stars}</text>{lines}'
except Exception:
 body='<text x="40" y="80" font-size="24">Stats will refresh after a successful API request.</text>'
def render(bg,fg): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 330" width="100%"><rect width="1000" height="330" rx="20" fill="{bg}"/><g fill="{fg}" font-family="Segoe UI,Ubuntu,Courier New,monospace">{body}</g></svg>'
os.makedirs("assets",exist_ok=True)
open("assets/stats-dark.svg","w",encoding="utf-8").write(render("#0b1020","#e5f7ff"))
open("assets/stats-light.svg","w",encoding="utf-8").write(render("#f8fafc","#111827"))
