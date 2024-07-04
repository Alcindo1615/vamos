import os
import time
import json
import csv
import random
os.system('cls')

def cargarDatos():
    with open('empleados.json', 'r', encoding='utf-8') as archivoEmpleados:
        empleados = json.load(archivoEmpleados)
    with open('tiendas.json', 'r', encoding='utf-8') as archivoTiendas:
        tiendas = json.load(archivoTiendas)
    with open('ventas.json', 'r', encoding='utf-8') as archivoVentas:
        ventas = json.load(archivoVentas)
    return empleados, tiendas, ventas


def guardarVenta(ventas):
    with open('ventas.json', 'w', encoding='utf-8') as archivoGuardar:
        json.dump(ventas, archivoGuardar, ensure_ascii=False, indent=4)
    
def crearCSV(estadisticas):
    with open('ESTADISTICA.csv', 'w', newline='\n', encoding='utf-8') as archivoCSV:
        escribir = csv.writer(archivoCSV)
        escribir.writerow(estadisticas)
        escribir.writerow([estadisticas['total_venta'], estadisticas['venta_minimo'], estadisticas['promedio_venta']])
        

def crearTXT(estadisticas):
    with open('ESTADISTICA.txt', 'w') as archivoTXT:
        archivoTXT.write(f'VENTA TOTAL: {estadisticas['total_venta']}\n')
        archivoTXT.write(f'VENTA MINIMA: {estadisticas['venta_minimo']}\n')
        archivoTXT.write(f'PROMEDIO VENTA: {estadisticas['promedio_venta']}\n')


def idVenta(ventas):
    id_venta = 0
    for venta in ventas['ventas']:
        if int(venta['id_venta']) > id_venta:
            id_venta = int(venta['id_venta'])
    return id_venta

def precargarVentas(empleados, ventas):
    id_venta = idVenta(ventas)
    nuevaVenta = {}
    for i in range(5):
        id_venta += 1
        empleado = random.choice(empleados)
        id_empleado = empleado['id_vendedor']
        id_tienda = empleado['id_tienda']
        mes = 'AGOSTO'
        total_venta = random.choice(range(50_000,200_000,100))
        nuevaVenta = {
            "id_venta": id_venta,
            "empleado": id_empleado,
            "id_tienda": id_tienda,
            "mes": mes,
            "total_venta": total_venta
        }
        ventas['ventas'].append(nuevaVenta)
        guardarVenta(ventas)
    print(ventas)

def crearVenta(empleados, tiendas, ventas):
    id_venta = idVenta(ventas)
    menub = True
    while menub:
        print('Ingrse el ID de la tienda que desea realizar la venta')
        for tienda in tiendas:
            print(f'ID: {tienda['id_tienda']} - {tienda['nombre']}')
        try:
            opcTienda = int(input('Ingrse el ID de la tienda o "6" para salir: '))
            if opcTienda < 1 or opcTienda > 6:
                errorRango()
            else:
                if opcTienda > 0 and opcTienda < 6:
                    limpiar()
                    print('Seleccione el ID del vendedor')
                    for empleado in empleados:
                        if empleado['id_tienda'] == opcTienda:
                            print(f'ID: {empleado['id_vendedor']} -->> {empleado['nombre']} {empleado['apellido']}')
                    print('----------------------------------')
                    try:
                        opcionVendedor = input('Ingrese el ID del vendedor: ')
                    except:
                        errorLetra()
                    id_venta += 1
                    mes = 'AGOSTO'
                    total_venta = int(input('Ingres el monto de la venta: '))
                    nuevaVenta = {
                        "id_venta": id_venta,
                        "empleado": opcionVendedor,
                        "id_tienda": opcTienda,
                        "mes": mes,
                        "total_venta": total_venta
                    }
                    ventas['ventas'].append(nuevaVenta)
                    guardarVenta(ventas)
                    os.system('cls')
                    print('Venta agregada de manera exitosa')
                    time.sleep(2)
                    menub = False
                else: break
        except:
            errorLetra()

def reporteSueldo(empleados, ventas):
    for empleado in empleados:
        total_venta = 0
        bono = 0
        salud = int(empleado['sueldo_base']*0.07)
        afp = int(empleado['sueldo_base']*0.12)
        for venta in ventas['ventas']:
            if venta['empleado'] == empleado['id_vendedor']:
                total_venta = total_venta + venta['total_venta']
        if total_venta >= 20_000_000:
            bono = int(empleado['sueldo_base']*0.02)
        elif total_venta >= 10_000_000:
            bono = int(empleado['sueldo_base']*0.01)
        elif total_venta >= 5_000_000:
            bono = int(empleado['sueldo_base']*0.05)
        sueldoLiquido = int(empleado['sueldo_base']-salud-afp) + bono
        print(f'Nombre: {empleado['nombre']} {empleado['apellido']} | Sueldo Base: {empleado['sueldo_base']} | Bono: {bono} | Desc. Salud: {salud} | Desc. AFP: {afp} | Sueldo Liquido: {sueldoLiquido}')

def estadisticas(ventas):
    total_venta = sum([venta['total_venta'] for venta in ventas['ventas']])
    venta_minimo = min([venta['total_venta'] for venta in ventas['ventas']])
    promedio_venta = int(total_venta/len(ventas['ventas']))

    print(f'Total venta: ${total_venta}')
    print(f'Venta minimo: ${venta_minimo}')
    print(f'Promedio venta: ${promedio_venta}')

    estadisticas = {
        'total_venta': total_venta,
        'venta_minimo': venta_minimo,
        'promedio_venta': promedio_venta
    }

    exportar = input('\nDesea exportar los datos a CSV y TXT ? (s/n): ')
    if exportar.lower() == 's':
        crearCSV(estadisticas)
        crearTXT(estadisticas)
        print('\nLos datos fueron exportados con exito')
        display()
    else:
        pass


def menuGeneral():
    print('-------- MENU GENERAL -------')
    print('[1] precargar ventas y guardar ventas.json')
    print('[2] crear nueva venta')
    print('[3] reporte de sueldo')
    print('[4] ver estadistica por tienda')
    print('[5] salir')

def limpiar():
    os.system('cls')

def display():
    time.sleep(1.5)

def errorLetra():
    print('*** La opción debe ser númerica ***')
    display()
    limpiar()

def errorRango():
    print('*** La opción esta fuera de rango ***')
    display()
    limpiar()

def main():
    empleados, tiendas, ventas = cargarDatos()
    menu = True
    while menu:
        menuGeneral()
        opc1 = 0
        try:
            opc1 = int(input('\nIngrese una opción: '))
            if opc1 < 1 or opc1 > 5:
                errorRango()
            else:
                if opc1 == 1:
                    precargarVentas(empleados, ventas)
                elif opc1 == 2:
                    crearVenta(empleados, tiendas, ventas)
                elif opc1 == 3:
                    reporteSueldo(empleados, ventas)
                elif opc1 == 4:
                    estadisticas(ventas)   
                elif opc1 == 5:
                    limpiar()
                    print('<<< ¡Hasta Pronto! >>>')
                    display()
                    limpiar()
                    menu = False
        except:
            errorLetra()
if __name__ == '__main__':
    main()