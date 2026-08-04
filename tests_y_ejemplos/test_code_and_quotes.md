# Pruebas de Bloques de Código y Citas

Este archivo de prueba sirve para evaluar cómo el conversor y el previsualizador renderizan bloques de código en múltiples lenguajes y estructuras de citas anidadas.

---

## 1. Bloques de Código (Stress Test)

### 1.1 Código Python (Script de red)
Un script de Python que utiliza asincronía para descargar páginas, ideal para verificar sangrías y espaciado de bloque.

```python
import asyncio
import aiohttp

async def download_page(session, url):
    print(f"Iniciando descarga de {url}")
    try:
        async with session.get(url, timeout=5) as response:
            status = response.status
            content = await response.text()
            print(f"Completado {url} con estado {status}")
            return content[:100]  # Retornar primer fragmento
    except Exception as e:
        print(f"Error descargando {url}: {e}")
        return None

async def main(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [download_page(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        print(f"Procesadas {len(results)} páginas con éxito.")

if __name__ == "__main__":
    lista_urls = [
        "https://python.org",
        "https://peps.python.org",
        "https://docs.python.org",
    ]
    asyncio.run(main(lista_urls))
```

### 1.2 Código Rust (Servidor Web simple)
Un ejemplo en Rust para validar palabras clave de tipado y sintaxis avanzada.

```rust
use std::net::TcpListener;
use std::net::TcpStream;
use std::io::prelude::*;
use std::fs;

fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();
    println!("Servidor Rust escuchando en el puerto 7878...");

    for stream in listener.incoming() {
        let stream = stream.unwrap();
        handle_connection(stream);
    }
}

fn handle_connection(mut stream: TcpStream) {
    let mut buffer = [0; 1024];
    stream.read(&mut buffer).unwrap();

    let get = b"GET / HTTP/1.1\r\n";
    let (status_line, filename) = if buffer.starts_with(get) {
        ("HTTP/1.1 200 OK", "index.html")
    } else {
        ("HTTP/1.1 404 NOT FOUND", "404.html")
    };

    let contents = fs::read_to_string(filename).unwrap_or_else(|_| "Error al cargar la página".to_string());
    let response = format!(
        "{}\r\nContent-Length: {}\r\n\r\n{}",
        status_line,
        contents.len(),
        contents
    );

    stream.write_all(response.as_bytes()).unwrap();
    stream.flush().unwrap();
}
```

---

## 2. Citas Anidadas (Blockquotes)

### 2.1 Cita normal
> Las computadoras son buenas siguiendo instrucciones, pero no leyendo tu mente.
>
> — Donald Knuth

### 2.2 Estructura de citas múltiples
Evaluamos la indentación progresiva y las barras verticales de las citas anidadas.

> Nivel principal de la conversación.
> 
>> Nivel secundario en respuesta al principal.
>>
>>> Tercer nivel de profundidad de respuesta, ideal para comprobar que no se desborde el margen derecho en las hojas A4.
>>>
>>> También soporta código inline como `x = y + z`.
>>
>> Volviendo al segundo nivel de profundidad.
