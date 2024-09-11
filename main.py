import flet as ft
import requests

def main(page: ft.Page):
    page.title = "Conectando con API"

    def get_teachers():
        url = "http://127.0.0.1:8000/api/teachers/search"
        response = requests.post(url)
        return response.json().get('data', [])

    def get_teacher_by_id(teacher_id):
        url = "http://127.0.0.1:8000/api/teachers/search"
        response = requests.post(url, json={"id": teacher_id})
        data = response.json().get('data', [])
        return data[0] if data else None

    def show_main_screen(e=None):
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombre1")),
                ft.DataColumn(ft.Text("Nombre2")),
                ft.DataColumn(ft.Text("Apellido1")),
                ft.DataColumn(ft.Text("Apellido2")),
                ft.DataColumn(ft.Text("Cedula")),
                ft.DataColumn(ft.Text("Telefono")),
                ft.DataColumn(ft.Text("Direccion")),
                ft.DataColumn(ft.Text("Correo")),
                ft.DataColumn(ft.Text("Acciones"))
            ],
            rows=[]
        )

        def update_table(e=None):
            teachers_data = get_teachers()
            table.rows.clear()
            if teachers_data:
                for teacher in teachers_data:
                    table.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(teacher["id"]))),
                                ft.DataCell(ft.Text(teacher["nombre1"])),
                                ft.DataCell(ft.Text(teacher["nombre2"])),
                                ft.DataCell(ft.Text(teacher["apellido1"])),
                                ft.DataCell(ft.Text(teacher["apellido2"])),
                                ft.DataCell(ft.Text(teacher["cedula"])),
                                ft.DataCell(ft.Text(teacher["telefono"])),
                                ft.DataCell(ft.Text(teacher["direccion"])),
                                ft.DataCell(ft.Text(teacher["correo"])),
                                ft.DataCell(
                                    ft.Row(
                                        [
                                            ft.IconButton(
                                                icon=ft.icons.EDIT,
                                                on_click=lambda e, teacher_id=teacher["id"]: edit_teacher(teacher_id)
                                            ),
                                            ft.IconButton(
                                                icon=ft.icons.DELETE,
                                                on_click=lambda e, teacher_id=teacher["id"]: delete_teacher(teacher_id)
                                            )
                                        ]
                                    )
                                ),
                            ]
                        )
                    )
                page.update()
            else:
                print("No hay profesores en la API")

        def delete_teacher(teacher_id):
            url = "http://127.0.0.1:8000/api/teachers"
            response = requests.delete(url, json={"resources": [teacher_id]})
            if response.status_code == 200:
                update_table()
                print(f"Profesor con ID {teacher_id} eliminado exitosamente.")
            else:
                print(f"Error al eliminar el profesor con ID {teacher_id}: {response.status_code}")

        def edit_teacher(teacher_id):
            teacher = get_teacher_by_id(teacher_id)
            if teacher:
                show_edit_screen(teacher)
            else:
                print(f"Error al obtener los datos del profesor con ID {teacher_id}: No encontrado")

        update_button = ft.ElevatedButton("Cargar Profesores", on_click=update_table)
        register_button = ft.ElevatedButton("Registrar Nuevo Profesor", on_click=lambda _: page.go("/register"))

        page.controls.clear()
        page.add(
            ft.Text("Lista de Profesores", size=24, weight=ft.FontWeight.BOLD),
            update_button,
            table,
            register_button
        )
        page.update()

    def show_register_screen(e=None):
        result_message = ft.Text("", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN)

        def register_teacher(e):
            teacher_data = {
                "mutate": [
                    {
                        "operation": "create",
                        "attributes": {
                            "id": id_input.value,
                            "nombre1": nombre1_input.value,
                            "nombre2": nombre2_input.value,
                            "apellido1": apellido1_input.value,
                            "apellido2": apellido2_input.value,
                            "cedula": cedula_input.value,
                            "telefono": telefono_input.value,
                            "direccion": direccion_input.value,
                            "correo": correo_input.value
                        },
                        "relations": []
                    }
                ]
            }

            url = "http://127.0.0.1:8000/api/teachers/mutate"
            response = requests.post(url, json=teacher_data)
            if response.status_code == 200:
                result_message.value = "Profesor registrado exitosamente."
                clear_form()
                page.update()
            else:
                result_message.value = f"Error al registrar el profesor: {response.status_code}"
                page.update()

        def clear_form():
            id_input.value = ""
            nombre1_input.value = ""
            nombre2_input.value = ""
            apellido1_input.value = ""
            apellido2_input.value = ""
            cedula_input.value = ""
            telefono_input.value = ""
            direccion_input.value = ""
            correo_input.value = ""
            page.update()

        id_input = ft.TextField(label="ID", width=150)
        nombre1_input = ft.TextField(label="Nombre 1", width=150)
        nombre2_input = ft.TextField(label="Nombre 2", width=150)
        apellido1_input = ft.TextField(label="Apellido 1", width=150)
        apellido2_input = ft.TextField(label="Apellido 2", width=150)
        cedula_input = ft.TextField(label="Cédula", width=150)
        telefono_input = ft.TextField(label="Teléfono", width=150)
        direccion_input = ft.TextField(label="Dirección", width=150)
        correo_input = ft.TextField(label="Correo", width=150)

        register_button = ft.ElevatedButton("Registrar Profesor", on_click=register_teacher)
        back_button = ft.ElevatedButton("Volver a la Lista", on_click=lambda _: page.go("/"))

        page.controls.clear()
        page.add(
            ft.Text("Registrar Nuevo Profesor", size=20, weight=ft.FontWeight.BOLD),
            id_input, nombre1_input, nombre2_input, apellido1_input, apellido2_input,
            cedula_input, telefono_input, direccion_input, correo_input,
            register_button,
            result_message,
            back_button
        )
        page.update()

    def show_edit_screen(teacher):
        result_message = ft.Text("", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN)

        def update_teacher(e):
            teacher_data = {
                "mutate": [
                    {
                        "operation": "update",
                        "key": teacher["id"],
                        "attributes": {
                            "nombre1": nombre1_input.value,
                            "nombre2": nombre2_input.value,
                            "apellido1": apellido1_input.value,
                            "apellido2": apellido2_input.value,
                            "cedula": cedula_input.value,
                            "telefono": telefono_input.value,
                            "direccion": direccion_input.value,
                            "correo": correo_input.value
                        },
                        "relations": []
                    }
                ]
            }

            url = "http://127.0.0.1:8000/api/teachers/mutate"
            response = requests.post(url, json=teacher_data)
            if response.status_code == 200:
                response_data = response.json()
                if "updated" in response_data and int(teacher["id"]) in response_data["updated"]:
                    result_message.value = "Profesor actualizado exitosamente."
                    clear_form()
                    # Aquí se realiza la navegación a la pantalla principal
                else:
                    result_message.value = "Error al actualizar el profesor: No se actualizó."
            else:
                error_details = response.json() if response.content else response.text
                result_message.value = f"Error al actualizar el profesor: {response.status_code} - {error_details}"
            page.update()

        def clear_form():
            id_input.value = ""
            nombre1_input.value = ""
            nombre2_input.value = ""
            apellido1_input.value = ""
            apellido2_input.value = ""
            cedula_input.value = ""
            telefono_input.value = ""
            direccion_input.value = ""
            correo_input.value = ""
            page.update()

        id_input = ft.TextField(label="ID", width=150, value=teacher["id"], read_only=True)
        nombre1_input = ft.TextField(label="Nombre 1", width=150, value=teacher["nombre1"])
        nombre2_input = ft.TextField(label="Nombre 2", width=150, value=teacher["nombre2"])
        apellido1_input = ft.TextField(label="Apellido 1", width=150, value=teacher["apellido1"])
        apellido2_input = ft.TextField(label="Apellido 2", width=150, value=teacher["apellido2"])
        cedula_input = ft.TextField(label="Cédula", width=150, value=teacher["cedula"])
        telefono_input = ft.TextField(label="Teléfono", width=150, value=teacher["telefono"])
        direccion_input = ft.TextField(label="Dirección", width=150, value=teacher["direccion"])
        correo_input = ft.TextField(label="Correo", width=150, value=teacher["correo"])

        update_button = ft.ElevatedButton("Actualizar Profesor", on_click=update_teacher)
        
        # El botón de retorno se configura para cambiar a la pantalla principal
        back_button = ft.ElevatedButton("Volver a la Lista", on_click=lambda e: show_main_screen())

        page.controls.clear()
        page.add(
            ft.Text("Editar Profesor", size=20, weight=ft.FontWeight.BOLD),
            id_input, nombre1_input, nombre2_input, apellido1_input, apellido2_input,
            cedula_input, telefono_input, direccion_input, correo_input,
            update_button,
            result_message,
            back_button
        )
        page.update()

    # Manejo de cambios de ruta
    page.on_route_change = lambda e: show_main_screen() if page.route == "/" else show_register_screen() if page.route == "/register" else show_edit_screen(get_teacher_by_id(int(page.route.split("/")[-1]))) if page.route.startswith("/edit/") else None

    page.go("/")

ft.app(target=main, view=ft.AppView.WEB_BROWSER)
