import re
from generate_clean_torso import generate_clean_chart

def apply():
    new_svg = generate_clean_chart()
    
    with open('tools/create_cv_chart.py', 'r', encoding='utf-8') as f:
        code = f.read()

    # Replace SVG_TORSO_ARTWORK
    pattern = r'SVG_TORSO_ARTWORK = """.*?"""'
    replacement = 'SVG_TORSO_ARTWORK = """' + new_svg + '"""'
    code = re.sub(pattern, replacement, code, flags=re.DOTALL)

    with open('tools/create_cv_chart.py', 'w', encoding='utf-8') as f:
        f.write(code)

    print("Updated tools/create_cv_chart.py!")

if __name__ == '__main__':
    apply()
