from bs4 import BeautifulSoup
import cssutils
import logging

cssutils.log.setLevel(logging.CRITICAL)
cssutils.ser.prefs.useDefaults()

def check_html(html_content, student_name):
    soup = BeautifulSoup(html_content, 'html.parser')
    score = 0
    feedback = []

    # 1. Estructura HTML + Etiquetas de metadatos (20 pts)
    title = soup.title
    author = soup.find('meta', attrs={'name': 'author'})
    css_link = soup.find('link', attrs={'href': 'stylesheets/estilo.css'})
    
    if title and title.string == student_name:
        score += 7
    elif title:
        score += 5
        feedback.append("Título de página incorrecto")
    else:
        feedback.append("Falta el título de página")

    if author and author.get('content') == student_name:
        score += 7
    elif author:
        score += 5
        feedback.append("Etiqueta de autor incorrecta")
    else:
        feedback.append("Falta la etiqueta de autor")

    if css_link:
        score += 6
    else:
        feedback.append("Falta la referencia al archivo CSS")

    # 2. Título de primer nivel (3 pts)
    h1 = soup.find('h1')
    if h1 and h1.text == student_name:
        score += 3
    else:
        feedback.append("Falta o es incorrecto el título de primer nivel")

    # 3. Secciones con subtítulos (10 pts)
    sections = soup.find_all('section')
    expected_sections = ['T01', 'T02', 'T03', 'T04']
    if len(sections) == 4 and all(s.find('h2') and s.find('h2').text in expected_sections for s in sections):
        score += 10
    elif len(sections) == 4:
        score += 7
        feedback.append("Secciones presentes pero con subtítulos incorrectos")
    else:
        feedback.append("Faltan secciones o están mal estructuradas")

    # 4. Panel de navegación (10 pts)
    nav = soup.find('nav')
    if nav and nav.find('ul') and len(nav.find_all('a')) == 4:
        score += 10
    elif nav and nav.find('ul'):
        score += 8
        feedback.append("Panel de navegación incompleto")
    else:
        feedback.append("Falta el panel de navegación o está mal estructurado")

    # 5. Pie de página (3 pts)
    footer = soup.find('footer')
    if footer and "P02 - PAO I 2024" in footer.text:
        score += 3
    else:
        feedback.append("Falta el pie de página o es incorrecto")

    # 6. Imagen en sección T01 (10 pts)
    t01_section = soup.find('section', id='T01')
    if t01_section:
        img = t01_section.find('img', alt="How to Grow and Care for 'Bosc' Pears")
        if img and img.find_parent('div'):
            score += 10
        elif img:
            score += 7
            feedback.append("Imagen presente pero no dentro de un contenedor")
        else:
            feedback.append("Falta la imagen en la sección T01 o tiene un texto alternativo incorrecto")
    else:
        feedback.append("Falta la sección T01")

    return score, feedback

def check_css(css_content):
    score = 0
    feedback = []
    stylesheet = cssutils.parseString(css_content)

    # 7. Importar fuente externa (5 pts)
    import_found = any(
        rule.type == rule.IMPORT_RULE and 'https://fonts.googleapis.com/css?family=Reddit+Mono' in rule.href
        for rule in stylesheet.cssRules
    )
    if import_found:
        score += 5
    else:
        feedback.append("Falta importar la fuente Reddit Mono")

    # 8. Selector universal + propiedad (9 pts)
    universal_selector = [r for r in stylesheet.cssRules if r.type == cssutils.css.CSSRule.STYLE_RULE]
    if any(r.selectorText == '*' and 'font-family: "Reddit Mono"' in r.style.cssText for r in universal_selector):
        score += 9
    else:
        feedback.append("Falta el selector universal con la propiedad de fuente")

    # 9. Acceder a título por selector de identificación (15 pts)
    h1_styles = [r for r in universal_selector if r.selectorText == '#titulo']
    if h1_styles:
        if all(prop in h1_styles[0].style.cssText for prop in [
            'font-family: "Segoe UI", sans-serif', 
            'font-size: 1.1rem', 
            'color: #53F072'
        ]):
            score += 15
        else:
            score += 10
            feedback.append("Estilos del #titulo incompletos")
    else:
        feedback.append("Falta el selector de identificación para #titulo")

    # 10. Acceder a imagen por selector de clase (15 pts)
    img_styles = [r for r in universal_selector if r.selectorText == '.imagen']
    if img_styles:
        required_props = [
            'margin: 0.2px 1.2rem', 
            'padding: 0 25%', 
            'border: 1px blue double', 
            'background-color: #E2F3DF'
        ]
        if all(prop in img_styles[0].style.cssText for prop in required_props):
            score += 15
        else:
            score += 10
            feedback.append("Propiedades de la imagen incompletas")
    else:
        feedback.append("Falta el selector de clase para .imagen")

    return score, feedback

def main(html_file, css_file, student_name):
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    with open(css_file, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    html_score, html_feedback = check_html(html_content, student_name)
    css_score, css_feedback = check_css(css_content)
    
    total_score = html_score + css_score
    
    print(f"Puntuación total: {total_score}/100")
    print("\nRetroalimentación HTML:")
    for item in html_feedback:
        print(f"- {item}")
    
    print("\nRetroalimentación CSS:")
    for item in css_feedback:
        print(f"- {item}")

if __name__ == "__main__":
    main('index.html', 'stylesheets/estilo.css', 'Ramirez Ramirez Jair Alexandre')
