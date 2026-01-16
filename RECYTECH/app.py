# LIBRERIAS
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# CONFIGURACION APP
app =Flask(__name__)

# CONFIGURACION DE LA BASE DE DATOS
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///recytech.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

# MODELO DE BASES DE DATOS 
class Residuo(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    tipo=db.Column(db.String(100), nullable=False)
    descripcion=db.Column(db.String(300), nullable=False)
    color=db.Column(db.String(50), nullable=False)
    ejemplos=db.Column(db.String(300))

# CREAR TABLAS
with app.app_context():
    db.create_all()

# RUTAS PRINCIPALES 

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/1")
def pagina1():
    return render_template("1.html")

@app.route("/2")
def pagina2():
    return render_template("2.html")

@app.route("/3")
def pagina3():
    return render_template("3.html")

@app.route("/4")
def pagina4():
    return render_template("4.html")

@app.route("/5")
def pagina5():
    return render_template("5.html")

@app.route("/6")
def pagina6():
    return render_template("6.html")

@app.route("/sopa")
def sopa():
    return render_template("sopa.html")

@app.route("/memorama")
def memorama():
    return render_template("memorama.html")



# FORMULARIO
@app.route("/formulario", methods=["GET", "POST"])
def formulario():
    residuo_consultado = None
    mensaje = ""

    if request.method == "POST":
        accion = request.form.get("accion")

        if accion == "agregar":
            nuevo_residuo = Residuo(
                tipo=request.form["tipo"],
                descripcion=request.form["descripcion"],
                color=request.form["color"],
                ejemplos=request.form.get("ejemplos", "")
            )
            db.session.add(nuevo_residuo)
            db.session.commit()
            mensaje = "Residuo agregado correctamente"

        elif accion == "consultar":
            id_buscar = request.form.get("id_consulta")

            if id_buscar:
                residuo_consultado = Residuo.query.get(id_buscar)
                if not residuo_consultado:
                    mensaje = "No se encontró un residuo con ese ID"
            else:
                mensaje = "Ingresa un ID válido"

    residuos = Residuo.query.all()

    return render_template(
        "formulario.html",
        residuos=residuos,
        residuo_consultado=residuo_consultado,
        mensaje=mensaje
    )


# CONSULTAS AVANZADAS 
@app.route("/consultas", methods=["GET", "POST"])
def consultas():
    resultados = []
    mensaje_consulta = None

    if request.method == "POST":
        criterio = request.form.get("criterio")
        valor = request.form.get("valor")

        if criterio and valor:
            columna = getattr(Residuo, criterio)
            resultados = Residuo.query.filter(columna.ilike(f"%{valor}%")).all()

            if not resultados:
                mensaje_consulta = "No se encontraron resultados"

    return render_template(
        "consultas.html",
        resultados=resultados,
        mensaje_consulta=mensaje_consulta
    )


@app.route("/eliminar", methods=["POST"])
def eliminar():
    id_residuo = request.form.get("id")

    if not id_residuo:
        return redirect(url_for("formulario"))

    residuo = Residuo.query.get(id_residuo)
    if residuo:
        db.session.delete(residuo)
        db.session.commit()

    return redirect(url_for("formulario"))

if __name__ == "__main__":
    app.run(debug=True)