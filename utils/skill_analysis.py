from .llm_utils import cliente


def analyze_career_transition(
    perfil_usuario, nuevo_puesto, modelo="llama-3.3-70b-versatile"
):
    """Compara habilidades actuales del usuario con las requeridas para el nuevo puesto"""
    prompt = f"""
        Actúa como un orientador laboral experto en análisis de habilidades transferibles.
        Usa EXCLUSIVAMENTE la información proporcionada en el perfil del usuario. No inventes experiencia laboral ni habilidades que no aparezcan en el texto.

        PERFIL DEL USUARIO (extraído de un CV):
        {perfil_usuario}

        OBJETIVO PROFESIONAL DEL USUARIO:
        {nuevo_puesto}

        Quiero que analices lo siguiente de forma completa y estructurada:

        1. Habilidades (técnicas y blandas) del usuario que son ÚTILES para el nuevo puesto. Incluye todos los detalles relevantes como: carnet de conducir, idiomas, certificaciones, estudios, herramientas, soft skills, etc.
        2. Habilidades o requisitos que le faltan para desempeñar ese puesto.
        3. Recomendaciones concretas de formación, experiencia o pasos prácticos.
        4. (Opcional) Otros roles intermedios que encajen con su perfil.

        NO inventes experiencia que no esté en el texto. NO asumas trabajos previos.

        Responde de forma clara y en formato de lista.
        """

    completion = cliente.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
    )
    return completion.choices[0].message.content


def compare_cvs_for_position(
    cv1_texto, cv2_texto, puesto_objetivo, modelo="llama-3.3-70b-versatile"
):
    """
    Compara dos CVs respecto a un puesto objetivo y devuelve cuál es más adecuado.
    """
    prompt = f"""
    Actúa como un orientador laboral experto. Tengo dos versiones de un CV y un puesto objetivo.

    CV1:
    {cv1_texto}

    CV2:
    {cv2_texto}

    Puesto objetivo: {puesto_objetivo}

    Analiza cada CV y responde:
    1. Qué habilidades relevantes ya tiene para el puesto.
    2. Qué habilidades faltan.
    3. Evalúa cuál CV se adapta mejor al puesto y explica por qué.
    4. Sugerencias para mejorar el CV menos adecuado.

    Responde de forma clara y estructurada.
    """
    completion = cliente.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
    )
    return completion.choices[0].message.content
