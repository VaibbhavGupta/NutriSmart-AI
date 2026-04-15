import os
from bs4 import BeautifulSoup

files = ['user_setup', 'dashboard', 'analyze_food', 'diet_planner', 'weekly_reports']
screens = []
head_html = ''

for i, f in enumerate(files):
    if not os.path.exists(f + '.html'):
        continue
    with open(f + '.html', 'r', encoding='utf-8') as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        if i == 0:
            head_html = str(soup.head)
        
        # rename body to div to avoid multiple body tags
        body = soup.body
        body.name = 'div'
        body['id'] = f
        body['class'] = body.get('class', []) + ['screen']
        if i > 0:
            body['style'] = 'display: none;'
            
        screens.append(str(body))

js = '''
<script>
    function navigate(screenId) {
        document.querySelectorAll('.screen').forEach(s => s.style.display = 'none');
        const target = document.getElementById(screenId);
        if (target) {
            target.style.display = 'block';
        }
        window.scrollTo(0, 0);
    }

    // Intercept clicks on links
    document.addEventListener('click', e => {
        const link = e.target.closest('a');
        if (link) {
            e.preventDefault();
            const text = link.innerText.toLowerCase();
            const icon = link.querySelector('.material-symbols-outlined');
            const iconText = icon ? icon.innerText.toLowerCase() : '';
            
            if (text.includes('dashboard') || iconText.includes('home')) navigate('dashboard');
            else if (text.includes('analyze') || iconText.includes('search')) navigate('analyze_food');
            else if (text.includes('planner') || iconText.includes('calendar_today')) navigate('diet_planner');
            else if (text.includes('reports') || iconText.includes('bar_chart')) navigate('weekly_reports');
            else navigate('user_setup'); // fallback
        }
        
        // Setup button 'Complete Setup' or Log Dinner
        const btn = e.target.closest('button');
        if (btn) {
            const text = btn.innerText.toLowerCase();
            if (text.includes('complete setup') || text.includes('get started')) {
                navigate('dashboard');
                e.preventDefault();
            } else if (text.includes('log dinner') || text.includes('add meal')) {
                navigate('analyze_food');
                e.preventDefault();
            }
        }
    });
</script>
'''

output = '<!DOCTYPE html>\n<html class="light" lang="en">\n' + head_html + '\n<body>\n'
output += '\n'.join(screens)
output += '\n' + js + '\n</body>\n</html>'

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(output)
print('index.html created successfully')
