from bs4 import BeautifulSoup
from selenium import webdriver
import undetected_chromedriver as uc
from time import sleep
import pandas as pd

# Función para extraer propiedades de la página web
def extract_properties(html):
    # Crear objeto BeautifulSoup para analizar el contenido HTML
    soup = BeautifulSoup(html, 'html.parser')
    # Encontrar todos los elementos de anuncios inmobiliarios
    items = soup.find_all("article", class_="item")

    properties = []

    # Iterar a través de cada anuncio inmobiliario
    for item in items:
        # Extraer información de título, precio, habitaciones, área y ascensor
        title = item.find("a", class_="item-link")["title"]
        price = item.find("span", class_="item-price").text.strip()

        details = item.find_all("span", class_="item-detail")
        rooms = details[0].text.strip()

        try:
            area = details[1].text.strip()
        except IndexError:
            area = "NA"

        elevator = False
        for detail in details:
            if "ascensor" in detail.text.lower():
                elevator = True
                break

        properties.append({"título": title, "precio": price, "habitaciones": rooms, "área": area, "ascensor": elevator})

    return properties

# Iniciar el navegador web utilizando undetected_chromedriver
driver = uc.Chrome(use_subprocess=True)

url_1 = 'https://www.idealista.com/venta-viviendas/palma-de-mallorca-balears-illes/pagina-{}.htm'

properties_1 = []

# Iterar a través de 30 páginas de anuncios de propiedades
for i in range(1, 30):
    print(f"Procesando página {i}")
    # Navegar a la página
    driver.get(url_1.format(i))
    # Establecer un tiempo de espera para permitir la carga de la
    # página y dar tiempo al usuario para resolver el CAPTCHA, si es
    # necesario
    driver.implicitly_wait(100)
    # Obtener el contenido HTML de la página
    html = driver.page_source
    # Extraer propiedades utilizando la función extract_properties()
    properties_1 += extract_properties(html)
    # Esperar 5 segundos antes de pasar a la siguiente página para evitar sobrecargar el servidor
    sleep(5)

# Cerrar el navegador
driver.close()

print(properties_1)

# Crear un DataFrame de pandas con las propiedades extraídas
properties_df = pd.DataFrame(properties_1)
# Guardar el DataFrame en un archivo CSV
properties_df.to_csv("properties_dataset.csv", index=False)