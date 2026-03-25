from redis import Redis


r = Redis(host='localhost', port=6379, decode_responses=True)

print(r.ping())

r.set('jedi2', 'Luke Skywalker')

print(r.get('jedi2'))

r.lpush('jedis', 'Yodaa', 'Obi- Wan', 'Mace Windu')

print(r.lrange('jedis', 0, -1))



# const { createClient } = require('redis');

# async function run() {
# // Configuración del cliente (host y puerto por defecto: localhost:6379)
# const client = createClient({
# url: 'redis://localhost:6379'
# });

# client.on('error', (err) => console.log('Redis Client Error', err));

# await client.connect();

# // 1. PING
# console.log(await client.ping()); // Imprime: PONG

# // 2. SET (Node.js devuelve strings por defecto si usas esta librería)
# await client.set('jedi2', 'Luke Skywalker');

# // 3. GET
# console.log(await client.get('jedi2')); // Imprime: Luke Skywalker

# // 4. LPUSH (acepta un array de elementos)
# await client.lPush('jedis', ['Yoda', 'Obi-Wan', 'Mace Windu']);

# // 5. LRANGE
# const jedis = await client.lRange('jedis', 0, -1);
# console.log(jedis); // Imprime el array de strings

# await client.disconnect();
# }

# run();