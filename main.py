from flask import Flask, render_template, request
from functions import functions as fc
from functions import parameters

app = Flask(__name__)


@app.route('/criadeira/home', methods=['GET', 'POST'])
def index():
    resultado = ''
    if request.method == 'POST':
        try:
            material = request.form.get('material')
            linha = request.form.get('linha')
            produzir = request.form.get('produzir')
            set_hora = request.form.get('set_hora')
            set_min = request.form.get('set_min')
            dia = request.form.get('dia')
            horas = request.form.get('horas')
            minutos = request.form.get('minutos')
            extra = request.form.get('extra') == 'on'
            periodo = request.form.get('periodo') == 'noturno'
            btn_tipo = request.form.get('acao')

            set_horas = f'{set_hora}:{set_min}:00'
            hora_inicio = f'{horas}:{minutos}:00'
            qtd_hora = fc.get_qty_hour(material.strip(), linha.strip())

            if qtd_hora == 'NP':
                resultado = 'Material não é produzido nesta linha!'
            else:
                if btn_tipo == 'confirmar':
                    minutos_dia = 648 if extra else 528
                    qtd_dia = (int(qtd_hora) / 60) * ((minutos_dia - 48) - (int(set_hora) * 60))
                    demanda = int(produzir) - int(qtd_dia)
                    if demanda < 0:
                        demanda = 'Demanda Atingida'
                        fim_producao = 'Concluído no mesmo dia'
                    else:
                        fim_producao = fc.calculate_production(
                            dia, hora_inicio, produzir, qtd_hora, set_horas, extra, periodo
                        )

                    resultado = f'''
                        Material: {fc.get_material_name(material)}<br>
                        Qtd. Hora: {qtd_hora} Unidades<br>
                        Qtd. Aproximada 1º dia: {int(qtd_dia)} Unidades<br>
                        Demanda prox. Dias: {demanda}<br>
                        Acabará em (Estimativa): {fim_producao}
                    '''

                elif btn_tipo == '24horas':
                    fim_producao = fc.calculate_production_in_24_hours(
                        dia, hora_inicio, produzir, qtd_hora, set_horas
                    )
                    resultado = f'''
                        Material: {fc.get_material_name(material)}<br>
                        Qtd. Hora: {qtd_hora} Unidades<br>
                        Acabará em (Estimativa): {fim_producao}
                    '''
        except Exception as e:
            resultado = f'Erro: {e}'

    return render_template(
        'public/criadeiras/templates/index.html',
        linhas=parameters.PRODUCTION_LINE,
        horas=fc.HOURS,
        minutos=fc.MINUTES,
        resultado=resultado,
        material_info=None
    )


@app.route('criadeira/buscar', methods=['POST'])
def buscar_material():
    codigo = request.form.get('codigo_busca')
    material_info = ''
    try:
        codigo_int = int(codigo)
        df = fc.load_dataBase()
        material = df[df['codigo'] == codigo_int]
        if material.empty:
            material_info = 'Material não encontrado.'
        else:
            row = material.iloc[0].to_dict()

            # Formulário com campos editáveis
            # Campo oculto para manter o código original
            material_info = '<form method="POST" action="/atualizar">'
            material_info += f'<input type="hidden" name="codigo" value="{row["codigo"]}">'

            for key, value in row.items():
                if key == 'codigo':
                    label = f'<label>{key}</label><input type="text" value="{value}" disabled>'
                else:
                    label = f'<label>{key}</label><input type="text" name="{key}" value="{value}">'
                material_info += label
            material_info += '''
                <button type="submit">Salvar</button>
            </form>
            '''
    except Exception as e:
        material_info = f'Erro ao buscar: {e}'

    return render_template(
        'public/criadeiras/templates/index.html',
        linhas=parameters.PRODUCTION_LINE,
        horas=fc.HOURS,
        minutos=fc.MINUTES,
        resultado='',
        material_info=material_info
    )

@app.route('criadeira/atualizar', methods=['POST'])
def atualizar_material():
    try:
        df = fc.load_dataBase()
        codigo = int(request.form.get('codigo'))

        # Garante que o material existe
        if codigo not in df['codigo'].values:
            return "Erro: Código não encontrado no banco de dados"

        # Atualiza os valores recebidos
        for coluna in df.columns:
            if coluna in request.form:
                novo_valor = request.form[coluna]
                if coluna == 'codigo':
                    continue  # não altera o código
                df.loc[df['codigo'] == codigo, coluna] = novo_valor

        # Salva de volta no Excel
        df.to_excel(r'database\database.xlsx', index=False)

        msg = "Dados atualizados com sucesso!"
    except Exception as e:
        msg = f"Erro ao atualizar: {e}"

    return render_template(
        'public/criadeiras/templates/index.html',
        linhas=parameters.PRODUCTION_LINE,
        horas=fc.HOURS,
        minutos=fc.MINUTES,
        resultado='',
        material_info=msg
    )


if __name__ == '__main__':
    app.run(debug=True)
