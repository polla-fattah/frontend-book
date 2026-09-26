import re

with open('public/_print/book/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

articles = re.findall(r'<div class=["\']([^"\']*td-[^"\']*)["\']', text)
print('td- classes found:', set(articles))

h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', text, re.DOTALL)
print(f'H1 headings ({len(h1s)}):')
for i, h in enumerate(h1s[:10]):
    clean = re.sub(r'<[^>]+>', ' ', h).strip()
    print(f'  {i+1}: {clean}')

# Look at how sections/articles are wrapped
matches = re.findall(r'(<(?:div|section|article)[^>]+id=["\']pg-[^"\']+["\'][^>]*>)', text)
print(f'\nElements with id="pg-...": {len(matches)}')
if matches:
    print('Sample match:', matches[0])

matches2 = re.findall(r'(<div class="td-content">)', text)
print(f'td-content occurrences: {len(matches2)}')
