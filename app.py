from flask import Flask, request, jsonify

from sqlalchemy import select
from flask_pydantic_spec import FlaskPydanticSpec

from models import *
from models import Clientes

app = Flask(__name__)
spec = FlaskPydanticSpec('flask',
                         title="API_Oficina",
                         version="1.0.0")

spec.register(app)
app.config['SECRET_KEY'] = 'secret'


@app.route('/novo_cliente', methods=['POST'])
def novo_cliente():
    """
        API para cadastrar clientes

        ## Endpoint:
        'novo_cliente'

        ## Parâmetros:
        - 'nome' - (str): Nome
        - 'cpf' - (str): CPF
        - 'telefone' - (str): Telefone
        - 'endereco' - (str): Endereço
            - ** Qualquer outro formato resultara em erro. **

        ## Resposta (JSON):
        ''' json
            {"nome": "laura",
            "cpf": "123-456-7890",
            "telefone": "123-456-7890",
            "endereco": "123-456-7890"}
        '''

        ## Erros possiveis:
        - Se algum erro for detetado, resultara em {"error": "Não foi possivel cadastrar este Usuario"}

        """
    try:
        dados = request.get_json()
        if not dados['nome'] or not dados['cpf'] or not dados['telefone'] or not dados['endereco']:
            return jsonify({"erro":"Preencha todos os campos"})
        else:
            cpf = dados['cpf'].strip()
            cpf_existe = db_session.query(Clientes).filter(Clientes.cpf == cpf).scalar()
            if cpf_existe:
                return jsonify({
                    "error": "Este CPF já esta cadastrado"
                }), 400


            telefone = dados['telefone'].strip()
            telef_existe = db_session.query(Clientes).filter(Clientes.telefone == telefone).scalar()
            if telef_existe:
                return jsonify({
                    "error": "Este numero de Telefone já esta cadastrado"
                }), 400


            form_novo_cliente = Clientes(
                nome=dados['nome'],
                cpf=int(dados['cpf'].strip()),
                telefone=dados['telefone'].strip(),
                endereco=dados['endereco']
            )

            form_novo_cliente.save()

        return jsonify({
            "Sucesso": "Cliente cadastrado com sucesso!",
            "Nome": dados['nome'],
            "CPF": int(dados['cpf'].strip()),
            "Telefone": dados['telefone'].strip(),
            "Endereço": dados['endereco']
        }), 201

    except ValueError:
        return jsonify({
            "error": "Não foi possivel cadastrar este Usuario"
        }), 400

    finally:
        db_session.close()


@app.route('/lista_clientes', methods=['GET']) #proteger
def lista_clientes():
    """
        API para listar clientes

        ## Endpoint:
        'lista_clientes'


        ## Erros possiveis:
        - Se algum erro for detetado, resultara em {"error": "Não foi possivel adicionar a lista"}

        """
    try:
        sql_lista_clientes = select(Clientes)
        resultado_clientes = db_session.execute(sql_lista_clientes).scalars().all()
        clientes = []
        for n in resultado_clientes:
            clientes.append(n.serialize_cliente())

        return jsonify({
            "lista_clientes": clientes
        }), 200

    except ValueError:
        return jsonify({
            "error": "Não foi possivel adicionar a lista"
        }), 400

    finally:
        db_session.close()


@app.route('/editar_cliente/<int:id_cliente>', methods=["POST"]) #proteger
def editar_cliente(id_cliente):
    """
        API para editar clientes

        ## Endpoint:
        'editar_cliente'

        ## Parâmetros:
        - 'nome' - (str): Nome
        - 'cpf' - (str): CPF
        - 'telefone' - (str): Telefone
        - 'endereco' - (str): Endereço
            - ** Qualquer outro formato resultara em erro. **

        ## Resposta (JSON):
        ''' json
            {"nome": "laura",
            "cpf": "123-456-7890",
            "telefone": "123-456-7890",
            "endereco": "123-456-7890"}
        '''

        ## Erros possiveis:
        - Se o formato para editar não for correto, resultara em {'error': 'Formato invalido'}

        """
    dados_editar_cliente = request.get_json()
    try:
        atualizacao_cliente = db_session.execute(select(Clientes).where(Clientes.id_cliente == id_cliente)).scalars().first()

        if not atualizacao_cliente:
            return jsonify({"Error":'Cliente não encontrado!'})

        if(not "nome" in  dados_editar_cliente or not "cpf" in dados_editar_cliente  or not "telefone" in dados_editar_cliente or not "endereco" in dados_editar_cliente):
            return jsonify({"Error":"Obrigatório preencher todos os campos"})

        cpf = dados_editar_cliente['cpf'].strip()
        if atualizacao_cliente.cpf != cpf:
            cpf_existe = db_session.query(Clientes).filter(Clientes.cpf == cpf).scalar()
            if cpf_existe:
                return jsonify({"error": "Este CPF já está cadastrado"})
        telefone = dados_editar_cliente['telefone'].strip()
        if atualizacao_cliente.telefone != telefone:
            telef_existe = db_session.query(Clientes).filter(Clientes.telefone == telefone).scalar()
            if telef_existe:
                return jsonify({
                    "error": "Este numero de Telefone já esta cadastrado"
                }), 400

        atualizacao_cliente.nome = dados_editar_cliente['nome']
        atualizacao_cliente.cpf = dados_editar_cliente['cpf'].strip()
        atualizacao_cliente.telefone = dados_editar_cliente['telefone'].strip()
        atualizacao_cliente.endereco = dados_editar_cliente['endereco']

        atualizacao_cliente.save()

        return jsonify({
            "Sucesso": "Cliente atualizado",
            "Nome": atualizacao_cliente.nome,
            "CPF": atualizacao_cliente.cpf,
            "Telefone": atualizacao_cliente.telefone,
            "Endereço": atualizacao_cliente.endereco,
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

    finally:
        db_session.close()



@app.route('/novo_veiculo', methods=['POST']) #proteger
def novo_veiculo():
    """
        API para cadastrar veiculos

        ## Endpoint:
        'novo_veiculo'

        ## Parâmetros:
        - 'marca' - (str): Marca
        - 'modelo' - (str): Modelo
        - 'placa' - (str): Placa
        - 'ano_fabri' - (int): Ano Fabricação
        - 'id_cliente' - (int): Id_cliente
            - ** Qualquer outro formato resultara em erro. **

        ## Resposta (JSON):
        ''' json
            {"marca": "FORD",
            "modelo": "New Fiesta",
            "placa": "FE90875",
            "ano_fabri": "2009",
            "id_cliente": "1"}
        '''

        ## Erros possiveis:
        - Se algum erro for detetado, resultara em {"error": "Não foi possivel cadastrar este Veiculo"}

        """
    try:
        dados = request.get_json()
        if not dados['marca'] or not dados['modelo'] or not dados['placa'] or not dados['ano_fabri'] or not dados['id_cliente']:
            return jsonify({"erro":"Preencha todos os campos"})
        else:
            placa = dados['placa'].strip()
            placa_existe = db_session.query(Veiculos).filter(Veiculos.placa == placa).scalar()
            if placa_existe:
                return jsonify({
                    "error": "Esta Placa já esta cadastrada"
                }), 400


            form_novo_veiculo = Veiculos(
                marca = dados['marca'],
                modelo = dados['modelo'],
                placa = dados['placa'],
                ano_fabri = int(dados['ano_fabri']),
                id_cliente = int(dados['id_cliente'])
            )

            form_novo_veiculo.save()

        return jsonify({
            "Sucesso": "Veiculo cadastrado com sucesso!",
            "Marca": dados['marca'],
            "Modelo": dados['modelo'],
            "Placa": dados['placa'],
            "Ano de fabricação": int(dados['ano_fabri']),
            "ID do Cliente": int(dados['id_cliente'])
            }), 201

    except ValueError:
        return jsonify({
            "error": "Não foi possivel cadastrar este Veiculo"
        }), 400

    finally:
        db_session.close()

@app.route('/lista_veiculos', methods=['GET']) #proteger
def lista_veiculos():
    """
        API para listar veiculos

        ## Endpoint:
        'lista_veiculos'


        ## Erros possiveis:
        - Se algum erro for detetado, resultara em {"error": "Não foi possivel adicionar a lista"}

        """
    try:
        sql_lista_veiculos = select(Veiculos)
        resultado_veiculos = db_session.execute(sql_lista_veiculos).scalars().all()
        veiculos = []
        for n in resultado_veiculos:
            veiculos.append(n.serialize_veiculo())

        return jsonify({
            "lista_veiculos": veiculos
        }), 200

    except ValueError:
        return jsonify({
            "error": "Não foi possivel adicionar a lista"
        }), 400

    finally:
        db_session.close()


@app.route('/editar_veiculo/<int:id_veiculo>', methods=["POST"]) #proteger
def editar_veiculo(id_veiculo):
    """
        API para editar veiculos

        ## Endpoint:
        'editar_veiculo'

        ## Parâmetros:
        - 'marca' - (str): Marca
        - 'modelo' - (str): Modelo
        - 'placa' - (str): Placa
        - 'ano_fabri' - (int): Ano Fabricação
            - ** Qualquer outro formato resultara em erro. **

        ## Resposta (JSON):
        ''' json
            {"marca": "FORD",
            "modelo": "New Fiesta",
            "placa": "FE90875",
            "ano_fabri": "2009"}
        '''

        ## Erros possiveis:
        - Se o formato para editar não for correto, resultara em {'error': 'Formato invalido'}

        """
    dados_editar_veiculo = request.get_json()
    try:
        atualizacao_veiculo = db_session.execute(select(Veiculos).where(Veiculos.id_veiculo == id_veiculo)).scalars().first()

        if not atualizacao_veiculo:
            return jsonify({"Error":'Veiculo não encontrado!'})

        if(not "marca" in  dados_editar_veiculo or not "modelo" in dados_editar_veiculo  or not "placa" in dados_editar_veiculo or not "ano_fabri" in dados_editar_veiculo):
            return jsonify({"Error":"Obrigatório preencher todos os campos"})

        placa = dados_editar_veiculo['placa'].strip()
        if atualizacao_veiculo.placa != placa:
            placa_existe = db_session.query(Veiculos).filter(Veiculos.placa == placa).scalar()
            if placa_existe:
                return jsonify({"error": "Esta Placa já está cadastrado"})


        atualizacao_veiculo.marca = dados_editar_veiculo['marca']
        atualizacao_veiculo.modelo = dados_editar_veiculo['modelo'].strip()
        atualizacao_veiculo.placa = dados_editar_veiculo['placa'].strip()
        atualizacao_veiculo.ano_fabri = dados_editar_veiculo['ano_fabri'].strip()

        atualizacao_veiculo.save()

        return jsonify({
            "Sucesso": "Veiculo atualizado",
            "Marca": atualizacao_veiculo.marca,
            "Modelo": atualizacao_veiculo.modelo,
            "Placa": atualizacao_veiculo.placa,
            "Ano de fabricação": atualizacao_veiculo.ano_fabri
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

    finally:
        db_session.close()



@app.route('/orden_servico', methods=['POST']) #proteger
def novo_servico():
    """
        API para cadastrar serviços

        ## Endpoint:
        'orden_serviço'

        ## Parâmetros:
        - 'veiculo' - (str): Veiculo
        - 'id_veiculo' - (int): Id_veiculo
        - 'data_abertura' - (str): Data de abertura
        - 'descricao' - (str): Descrição
        - 'status' - (str): Status
        - 'valor' - (float): Valor
            - ** Qualquer outro formato resultara em erro. **

        ## Resposta (JSON):
        ''' json
            {"Veiculo": "FORD",
            "id_veiculo": "1",
            "data_abertura": "22-06-2025",
            "descricao": "motor com problemas",
            "status": ""}
        '''

        ## Erros possiveis:
        - Se algum erro for detetado, resultara em {"error": "Não foi possivel cadastrar este serviço"}

        """
    try:
        dados = request.get_json()
        if not dados['veiculo'] or not dados ['id_veiculo'] or not  dados['data_abertura'] or not dados['descricao'] or not dados['status' ] or not dados['valor']:
            return jsonify({"erro":"Preencha todos os campos"})
        else:
            form_orden_servico = Ordens(
                veiculo=dados['veiculo'],
                id_veiculo=dados['id_veiculo'],
                data_abertura=dados['data_abertura'],
                descricao=dados['descricao'],
                status=dados['status'],
                valor=float(dados['valor'])
            )

            form_orden_servico.save()

        return jsonify({
            "Sucesso": "Cadastro realizado com sucesso!",
            "Veiculo": dados['veiculo'],
            "ID do veiculo":dados['id_veiculo'],
            "Data abertura":dados['data_abertura'],
            "Descrição":dados['descricao'],
            "Status":dados['status'],
            "Valor":float(dados['valor'])
        }), 201

    except ValueError:
        return jsonify({
            "error": "Não foi possivel cadastrar este serviço"
        }), 400

    finally:
        db_session.close()


@app.route('/lista_servicos', methods=['GET']) #proteger
def lista_ordens():
    """
        API para listar serviços

        ## Endpoint:
        'lista_serviços'


        ## Erros possiveis:
        - Se algum erro for detetado, resultara em {"error": "Não foi possivel adicionar a lista"}

        """
    try:
         sql_lista_ordens = select(Ordens)
         resultado_ordens = db_session.execute(sql_lista_ordens).scalars().all()
         ordens = []
         for n in resultado_ordens:
             ordens.append(n.serialize_orden())

             return jsonify({
                 "ordens_serviço": ordens
             }), 200

    except ValueError:
        return jsonify({
            "error": "Não foi possivel adicionar a lista"
        }), 400

    finally:
        db_session.close()


@app.route('/editar_orden/<int:id_orden>', methods=['POST']) #proteger
def editar_orden(id_orden):
    """
        API para editar serviços

        ## Endpoint:
        'editar_orden'

        ## Parâmetros:
        - 'veiculo' - (str): Veiculo
        - 'data_abertura' - (str): Data de abertura
        - 'descricao' - (str): Descrição
        - 'status' - (str): Status
        - 'valor' - (float): Valor
            - ** Qualquer outro formato resultara em erro. **

        ## Resposta (JSON):
        ''' json
            {"veiculo": "FORD",
            "data_abertura": "22-06-2025",
            "descricao": "motor com problemas",
            "status": ""
            "valor": 0,0}
        '''

        ## Erros possiveis:
        - Se o formato para editar não for correto, resultara em {'error': 'Formato invalido'}

        """
    dados_editar_orden= request.get_json()
    try:
        atualizacao_orden = db_session.execute(select(Ordens).where(Ordens.id_orden == id_orden)).scalars().first()

        if not atualizacao_orden:
            return jsonify({"Error": 'Ordem de serviço não encontrada!'})

        if (not "veiculo" in dados_editar_orden or not "data_abertura" in dados_editar_orden or not "descricao" in dados_editar_orden or not "valor" in dados_editar_orden):
            return jsonify({"Error": "Obrigatório preencher todos os campos"})

        atualizacao_orden.veiculo = dados_editar_orden['veiculo']
        atualizacao_orden.data_abertura = dados_editar_orden['data_abertura']
        atualizacao_orden.descricao = dados_editar_orden['descricao'].strip()
        atualizacao_orden.valor = dados_editar_orden['valor'].strip()

        atualizacao_orden.save()

        return jsonify({
            "Sucesso": "Serviço atualizado",
            "Veiculo": atualizacao_orden.veiculo,
            "Data de abertura": atualizacao_orden.data_abertura,
            "Descrição": atualizacao_orden.descricao,
            "Valor": atualizacao_orden.valor
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

    finally:
        db_session.close()


@app.route('/status/<var_status>', methods=['GET'])
def status(var_status):
    """
        API para mostrar o status

        ## Endpoint:
        'status'


        ## Erros possiveis:
        - Se algum erro for detetado, resultara em {"error": "Erro"}

        """
    try:
        sql_status = select(Ordens).where(Ordens.status == var_status)
        resultado_status = db_session.execute(sql_status).scalars()
        lista_status = []
        for status in resultado_status:
            lista_status.append(status.serialize_orden())
        return jsonify({
            "LISTA": lista_status
        }), 200

    except ValueError:
        return jsonify({
            "error": "Error"
        }), 400

    finally:
        db_session.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)