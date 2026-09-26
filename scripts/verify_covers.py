import re

with open('public/_print/book/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

covers = re.findall(r'<div class="td-book-cover-page[^"]*".*?</div>', text, re.DOTALL)
print(f'Covers found in print view: {len(covers)}')
for c in covers:
    print(c[:250])

with open('public/book/index.html', 'r', encoding='utf-8') as f:
    book_text = f.read()
book_covers = re.findall(r'<div class="row g-4 my-4 align-items-center justify-content-center d-print-none".*?</div>\s*</div>', book_text, re.DOTALL)
print(f'Covers found in book landing page: {len(book_covers)}')
