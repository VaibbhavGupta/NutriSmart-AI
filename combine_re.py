import re

files = ['user_setup', 'dashboard', 'analyze_food', 'diet_planner', 'weekly_reports']
screens_html = []
head_html = ''

for i, f in enumerate(files):
    try:
        with open(f + '.html', 'r', encoding='utf-8') as fp:
            content = fp.read()
            
            # Extract head from first file
            if i == 0:
                head_match = re.search(r'<head>(.*?)</head>', content, re.DOTALL | re.IGNORECASE)
                if head_match:
                    head_html = head_match.group(1)
            
            # Extract body
            body_match = re.search(r'<body(.*?)>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
            if body_match:
                body_attrs = body_match.group(1)
                body_content = body_match.group(2)
                
                # We need to extract the existing class attribute to apply it to our div wrapper
                class_match = re.search(r'class="([^"]+)"', body_attrs, re.IGNORECASE)
                classes = "screen"
                if class_match:
                    classes += " " + class_match.group(1)
                
                style = "" if i == 0 else "display: none;"
                
                screens_html.append(f'<div id="{f}" class="{classes}" style="{style}">\n{body_content}\n</div>')
    except Exception as e:
        print(f"Error processing {f}: {e}")

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

    // Intercept clicks on links and buttons
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

    // Run automatically if there's a hash
    window.addEventListener('load', () => {
        const hash = window.location.hash.substring(1);
        if (hash) {
            navigate(hash);
        }
    });
</script>
'''

output = '<!DOCTYPE html>\n<html class="light" lang="en">\n<head>\n' + head_html + '\n</head>\n<body class="bg-surface text-on-surface" style="margin: 0; padding: 0;">\n'
output += '\n'.join(screens_html)
output += '\n' + js + '\n</body>\n</html>'

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(output)
print('index.html created successfully')
