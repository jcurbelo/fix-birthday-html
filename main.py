import sys
import re

REGEX = r'(<\/?\w+)(=[^>]+)?>'
REPLACEMENTS = {
    'htlm': 'html',
}


def clean_tag(tag: str) -> str:
    for k, v in REPLACEMENTS.items():
        tag = tag.replace(k, v)
    tag = ' '.join(tag.split())
    return tag


def main():
    if len(sys.argv) < 2:
        print('Missing file_name argument, use script as "python main.y your_file.htlm')
        return
    file_name = sys.argv[1]
    with open(file_name, 'r') as f:
        txt = '\n'.join(f.readlines())

    result = ''
    matches = re.finditer(REGEX, txt, re.MULTILINE | re.IGNORECASE)
    for match in matches:
        current_tag = ''
        groups = [g for g in match.groups() if g]
        # no attr tag
        if len(groups) == 1:
            current_tag = clean_tag(groups[0])
            current_tag = '{}>'.format(current_tag)
        else:
            label = groups[0].replace('<', '')
            content = clean_tag(groups[1].replace('=', ''))
            # attr tag
            current_tag = '''
            <p>
                <b>{}:</b>
                <span>{}</span>
            </p>
            '''.format(label, content)

        result = '{}\n{}'.format(result, current_tag)

    output_file_name = '{}.html'.format(file_name.split('.')[0])

    with open(output_file_name, 'w') as f:
        f.write(result)


if __name__ == '__main__':
    main()
