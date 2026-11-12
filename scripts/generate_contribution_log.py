# Generates assets/solar-contribution.svg from the user's real contribution
# calendar (GraphQL). Runs locally and in Actions; stdlib only.
import base64, json, os, urllib.request, datetime

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'solar-contribution.svg')
USER = os.environ.get('USERNAME_REPO', 'abinash123hg')

def fetch_calendar(tok):
    to = datetime.datetime.now(datetime.timezone.utc).replace(hour=23, minute=59)
    frm = to - datetime.timedelta(days=364)
    q = '''query($u:String!,$f:DateTime!,$t:DateTime!){user(login:$u){contributionsCollection(from:$f,to:$t){contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}'''
    body = json.dumps({'query': q, 'variables': {'u': USER, 'f': frm.strftime('%Y-%m-%dT%H:%M:%SZ'), 't': to.strftime('%Y-%m-%dT%H:%M:%SZ')}}).encode()
    req = urllib.request.Request('https://api.github.com/graphql', data=body,
                                 headers={'Authorization': 'Bearer ' + tok, 'Content-Type': 'application/json',
                                          'User-Agent': 'contribution-log'})
    d = json.load(urllib.request.urlopen(req))
    weeks = d['data']['user']['contributionsCollection']['contributionCalendar']['weeks'][-26:]
    return weeks

def build_svg(weeks):
    per_week = [sum(x['contributionCount'] for x in w['contributionDays']) for w in weeks]
    days = [x for w in weeks for x in w['contributionDays']]
    total = sum(per_week)
    best_count = max(x['contributionCount'] for x in days)
    best_day = next(x['date'][:10] for x in days if x['contributionCount'] == best_count)
    streak = 0
    for x in reversed(days):
        if x['contributionCount'] > 0:
            streak += 1
        else:
            break
    longest = run = 0
    for x in days:
        run = run + 1 if x['contributionCount'] > 0 else 0
        longest = max(longest, run)
    mx = max(max(per_week), 1)
    bx, bw, bh, base = 30, 28, 66, 122
    bars = ''
    for i, v in enumerate(per_week):
        h = max(2, v / mx * bh)
        bars += f'<rect x="{bx + i*(bw+2)}" y="{base - h}" width="{bw}" height="{h}" rx="3" fill="#3fb950" opacity="{0.45 + 0.55*(h/bh)}"><title>{weeks[i]["contributionDays"][0]["date"][:10]} · {v} contributions</title></rect>'
    months = ''
    seen = set()
    for i, w in enumerate(weeks):
        m = w['contributionDays'][0]['date'][5:7]
        if m not in seen and int(w['contributionDays'][0]['date'][8:10]) <= 14:
            seen.add(m)
            months += f'<text x="{bx + i*(bw+2)}" y="136" font-size="8" fill="#6e7681">{datetime.date(2000,int(m),1).strftime("%b")}</text>'
    sub = 'I am the sun; my contributions are the light.'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="880" height="170" viewBox="0 0 880 170" role="img" aria-label="Contribution activity: last 26 weeks, {total} contributions, longest streak {longest} days, best day {best_count} commits">
<style>text{{font-family:'Segoe UI',system-ui,-apple-system,Helvetica,Arial,sans-serif}}</style>
<rect width="880" height="170" rx="14" fill="#0D1117" stroke="#30363d" stroke-width="1"/>
<text x="26" y="32" font-size="13" font-weight="700" letter-spacing="1" fill="#C9D1D9">CONTRIBUTION ACTIVITY · LAST 26 WEEKS</text>
<text x="854" y="32" font-size="11" font-weight="600" fill="#3fb950" text-anchor="end">{total} contributions</text>
{bars}
{months}
<line x1="30" y1="122" x2="{bx + 26*(bw+2) - 2}" y2="122" stroke="#30363d" stroke-width="1"/>
<text x="26" y="156" font-size="10.5" fill="#8b949e">current streak {streak} days · longest streak {longest} days · best day {best_count} commits ({best_day}) · real GitHub data, refreshed daily</text>
</svg>'''

if __name__ == '__main__':
    tok = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
    weeks = fetch_calendar(tok)
    svg = build_svg(weeks)
    open(OUT, 'w', encoding='utf-8').write(svg)
    total = sum(sum(x['contributionCount'] for x in w['contributionDays']) for w in weeks)
    print('wrote', OUT, len(svg), 'bytes · 26-week total', total)
