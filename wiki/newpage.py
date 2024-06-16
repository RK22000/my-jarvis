#!/usr/bin/env python3
"""
This script creates new [markdeep](https://casual-effects.com/markdeep/) pages.
Suppy this script with pages you want to make and it will make those pages as
markdeep pages. 

For instance
```shell
python newpage.py about blogs/accidental-rm-rf
```
will create two new markdeep pages
- about.md.html 
- blogs/accidental-rm-rf.md.html

> Protip, since this only uses standard library run `chmod u+x newpage.py` to
  make it so that you can call this scrip directly like 
  `./newpage.py about blogs/accidental-rm-rf`

"""
import argparse
import os

parser = argparse.ArgumentParser(
    # prog="New Page",
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter
)
parser.add_argument("newpages", nargs='+', help="New pages to create. Just \
                    write the page name. Don't bother with the extensions.")
parser.add_argument("--by", help="The person authoring these pages.")
def make_file(page: str, author: str = None):
    """
    Make a markdeep page and return the path to the page
    """
    name = os.path.basename(page)
    page += ".md.html"
    dirname = os.path.dirname(page)
    os.makedirs(dirname, exist_ok=True) if dirname != '' else None
    with open(page, 'w') as f:
        print(f'\t\t**{name}**', file=f)
        print(f'\t(Subheading), authored by {author}', file=f) if author is not None else print(f'\t(Subheading)', file=f)
        print('\n'*20, file=f)
        markdeep = r'<!-- Markdeep: --><style class="fallback">body{visibility:hidden;white-space:pre;font-family:monospace}</style><script src="markdeep.min.js" charset="utf-8"></script><script src="https://morgan3d.github.io/markdeep/latest/markdeep.min.js" charset="utf-8"></script><script>window.alreadyProcessedMarkdeep||(document.body.style.visibility="visible")</script>'
        print(markdeep, file=f)
    return page

if __name__=='__main__':
    args = parser.parse_args()
    # print(args)
    count = len(args.newpages)
    for i, page in enumerate(args.newpages):
        try:
            page = make_file(page, args.by)
        except Exception as e:
            page = f'XXX Failed with {e}'
        print(f'{f"{i+1}/{count}:":>5} {page}')

