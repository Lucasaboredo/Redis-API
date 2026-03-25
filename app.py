from flask import Flask, render_template, jsonify, request
import redis

app = Flask(__name__)

# Conexión a Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Lista estática de capítulos de The Mandalorian
EPISODES_DATA = {
    1: [
        {"ep": 1, "title": "Capítulo 1: El mandaloriano (The Mandalorian)"},
        {"ep": 2, "title": "Capítulo 2: El niño (The Child)"},
        {"ep": 3, "title": "Capítulo 3: El pecado (The Sin)"},
        {"ep": 4, "title": "Capítulo 4: Santuario (Sanctuary)"},
        {"ep": 5, "title": "Capítulo 5: El pistolero (The Gunslinger)"},
        {"ep": 6, "title": "Capítulo 6: El prisionero (The Prisoner)"},
        {"ep": 7, "title": "Capítulo 7: El ajuste de cuentas (The Reckoning)"},
        {"ep": 8, "title": "Capítulo 8: Redención (Redemption)"}
    ],
    2: [
        {"ep": 1, "title": "Capítulo 9: El mariscal (The Marshal)"},
        {"ep": 2, "title": "Capítulo 10: La pasajera (The Passenger)"},
        {"ep": 3, "title": "Capítulo 11: La heredera (The Heiress)"},
        {"ep": 4, "title": "Capítulo 12: El asedio (The Siege)"},
        {"ep": 5, "title": "Capítulo 13: La Jedi (The Jedi)"},
        {"ep": 6, "title": "Capítulo 14: La tragedia (The Tragedy)"},
        {"ep": 7, "title": "Capítulo 15: El creyente (The Believer)"},
        {"ep": 8, "title": "Capítulo 16: El rescate (The Rescue)"}
    ],
    3: [
        {"ep": 1, "title": "Capítulo 17: El apóstata (The Apostate)"},
        {"ep": 2, "title": "Capítulo 18: Las minas de Mandalore (The Mines of Mandalore)"},
        {"ep": 3, "title": "Capítulo 19: El converso (The Convert)"},
        {"ep": 4, "title": "Capítulo 20: El huérfano (The Foundling)"},
        {"ep": 5, "title": "Capítulo 21: El pirata (The Pirate)"},
        {"ep": 6, "title": "Capítulo 22: Pistoleros a sueldo (Guns for Hire)"},
        {"ep": 7, "title": "Capítulo 23: Los espías (The Spies)"},
        {"ep": 8, "title": "Capítulo 24: El regreso (The Return)"}
    ]
}

def get_all_episodes():
    episodes = []
    for s, eps in EPISODES_DATA.items():
        for ep_data in eps:
            e = ep_data["ep"]
            title = ep_data["title"]
            ep_id = f"S{s:02d}E{e:02d}"
            # Leer el estado de Redis
            estado = r.get(f"mando:ep:{ep_id}")
            if not estado:
                estado = "Disponible"
            
            episodes.append({
                "id": ep_id,
                "season": s,
                "episode": e,
                "title": title,
                "status": estado
            })
    return episodes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/episodes', methods=['GET'])
def list_episodes():
    try:
        r.ping() # Validar conexión
    except redis.exceptions.ConnectionError:
        return jsonify({"error": "No se pudo conectar a Redis Database"}), 500
        
    episodes = get_all_episodes()
    return jsonify(episodes)

@app.route('/api/episodes/<ep_id>/rent', methods=['POST'])
def rent_episode(ep_id):
    key = f"mando:ep:{ep_id}"
    
    # Intenta hacer Set si NO existe (NX) con expiración de 4 minutos (240 seg)
    # Retorna True si se aplicó, False si la key ya existía
    success = r.set(key, "Reservado", ex=240, nx=True)
    
    if success:
        return jsonify({"success": True, "message": "Capítulo reservado por 4 minutos para confirmar pago."})
    else:
        current_status = r.get(key)
        return jsonify({"success": False, "message": f"El capítulo actualmente está {current_status}."}), 400

@app.route('/api/episodes/<ep_id>/pay', methods=['POST'])
def confirm_payment(ep_id):
    data = request.json or {}
    price = data.get('price')
    
    # Validación simple del precio u otro dato.
    if not price:
        return jsonify({"success": False, "message": "Se requiere el precio para confirmar."}), 400
        
    key = f"mando:ep:{ep_id}"
    current_status = r.get(key)
    
    if current_status == "Reservado":
        # Confirmar alquiler por 24 horas (86400 seg)
        r.set(key, "Alquilado", ex=86400)
        return jsonify({"success": True, "message": "Pago confirmado. Capítulo alquilado por 24 horas."})
    elif current_status == "Alquilado":
        return jsonify({"success": False, "message": "El capítulo ya se encuentra alquilado."}), 400
    else:
        return jsonify({"success": False, "message": "Debe reservar el capítulo antes de pagar."}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
