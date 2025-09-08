from flask import Flask, request, jsonify

# O nome da sua aplicação Flask deve ser 'app'
# O nome do seu arquivo principal é 'boot.py'
app = Flask(__name__)

# O endpoint que receberá os webhooks da Evolution API
@app.route('/webhook', methods=['POST'])
def handle_webhook():
    try:
        # Recebe o JSON enviado pelo webhook
        data = request.json
        print("Webhook recebido:")
        print(data)

        # Verifica se o evento é uma nova mensagem
        if data and 'event' in data and data['event'] == 'messages.upsert':
            # Percorre a lista de mensagens no payload
            for message in data['data']:
                # Verifica se a mensagem foi recebida por sua instância (não enviada por ela)
                # 'fromMe': False é a forma de identificar mensagens recebidas
                if not message.get('key', {}).get('fromMe', False):
                    # Extrai os dados importantes da mensagem
                    message_text = message.get('message', {}).get('conversation', 'Mensagem não é texto')
                    sender_number = message.get('key', {}).get('remoteJid', 'Número desconhecido')

                    print(f"Nova mensagem de {sender_number}: {message_text}")
                    
                    # **********************************************
                    # ** Coloque aqui a sua lógica personalizada **
                    # ** (por exemplo, responder à mensagem, salvar em um banco de dados) **
                    # **********************************************
                    
        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print(f"Erro ao processar o webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# OBS: Não adicione app.run() aqui.
# A linha `app.run()` é usada apenas para rodar a aplicação localmente.
# O PythonAnywhere se encarrega de rodar a aplicação para você.